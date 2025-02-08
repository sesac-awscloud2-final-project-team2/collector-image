#!/bin/bash

source .env

# Update system packages
sudo yum update -y

sudo yum install docker -y
sudo systemctl start docker
sudo usermod -aG docker ec2-user
sudo yum install git -y

# Add Jenkins repository
sudo yum install wget -y
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

# Install Java
sudo dnf install java-17-amazon-corretto -y

# Install Jenkins
sudo yum install jenkins -y

# Start Jenkins service
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Wait for Jenkins to start
sleep 30

# Get initial admin password
JENKINS_PASSWORD=$(sudo cat /var/lib/jenkins/secrets/initialAdminPassword)

# Install Jenkins CLI
wget http://localhost:8080/jnlpJars/jenkins-cli.jar

# Install suggested plugins
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$JENKINS_PASSWORD install-plugin workflow-cps-global-lib github-organization-folder cloudbees-folder antisamy-markup-formatter build-timeout credentials-binding timestamper ws-cleanup ant gradle workflow-aggregator github-organization-folder pipeline-stage-view git subversion ssh-slaves matrix-auth pam-auth ldap email-ext mailer docker-build-step docker-plugin docker-workflow amazon-ecr pipeline-github

# Create admin user
echo "jenkins.model.Jenkins.instance.securityRealm.createAccount('admin', '${JENKINS_PASSWORD}')" | java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$JENKINS_PASSWORD groovy =

# Docker credential
sudo usermod -aG docker jenkins

# Restart Jenkins
sudo systemctl restart jenkins

# GitHub 토큰을 Global credentials로 추가
echo "<com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>
  <scope>GLOBAL</scope>
  <id>${GITHUB_USER}</id>
  <description>to-github-token</description>
  <username>${GITHUB_USER}</username>
  <password>${GITHUB_TOKEN}</password>
</com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>" | \
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$JENKINS_PASSWORD create-credentials-by-xml system::system::jenkins _

echo "<org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl>
  <scope>GLOBAL</scope>
  <id>github-token</id>
  <description>from-github-token</description>
  <secret>${GITHUB_TOKEN}</secret>
</org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl>" | \
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$JENKINS_PASSWORD create-credentials-by-xml system::system::jenkins _

# AWS 자격 증명을 Global credentials로 추가
echo "<com.cloudbees.jenkins.plugins.awscredentials.AWSCredentialsImpl>
  <scope>GLOBAL</scope>
  <id>ecr-credential</id>
  <description>AWS Credentials</description>
  <accessKey>${AWS_ACCESS_KEY}</accessKey>
  <secretKey>${AWS_SECRET_KEY}</secretKey>
</com.cloudbees.jenkins.plugins.awscredentials.AWSCredentialsImpl>" | \
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$JENKINS_PASSWORD create-credentials-by-xml system::system::jenkins _

echo "Jenkins setup complete. Access it at http://localhost:8080"
echo "Username: admin"
echo "Password: $JENKINS_PASSWORD"