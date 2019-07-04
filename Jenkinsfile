pipeline {
  agent any
  stages {
    stage('检出') {
      steps {
        checkout([$class: 'GitSCM', branches: [[name: env.GIT_BUILD_REF]], 
                                                                                                                                                            userRemoteConfigs: [[url: env.GIT_REPO_URL, credentialsId: env.CREDENTIALS_ID]]])
      }
    }
    docker.image('python:3.6.0') {
         stage("构建") {
                 echo "构建中..."
                 sh 'docker -version'              
                 echo "构建完成."                 
         }
         stage("测试") {
                 echo "单元测试中..."
                 sh 'python --version'            
                 echo "单元测试完成."
                 junit '*.xml' // 收集单元测试报告的调用过程
         }
         stage("部署") {
                 echo "部署中..."
                 // 请在这里放置收集单元测试报告的调用过程，例如:
                 // sh 'mvn tomcat7:deploy' // Maven tomcat7 插件示例：
                 // sh './deploy.sh' // 自研部署脚本
                 echo "部署完成"
         }
     }
  }
 }