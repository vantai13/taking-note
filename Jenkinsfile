pipeline {
    agent any
    environment {
        // Tên image trên ECR
        FULL_IMAGE = "954692413669.dkr.ecr.ap-southeast-1.amazonaws.com/taking-note-app:ver-${BUILD_ID}"
        
        // ✅ SỬA LẠI TASK FAMILY CHO ĐÚNG VỚI DỰ ÁN FLASK
        TASK_FAMILY = "taking-note-app-task-def" 
        
        // Các biến tạm thời, không cần sửa
        TASK_DEFINITION = ""
        NEW_TASK_DEFINITION = ""
        NEW_TASK_INFO = ""
        NEW_REVISION = ""
    }
    stages {
        // stage('Checkout') {
        //     steps {
                
        //         git 'https://github.com/vantai13/taking-note.git' 
        //     }
        // }

        stage('Build') {
            steps {
                sh 'docker build -t taking-note-app:ver-${BUILD_ID} .'
            }
        }
        
        stage('Upload image to ECR') {
            steps {
                sh 'aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 954692413669.dkr.ecr.ap-southeast-1.amazonaws.com'
                sh 'docker tag taking-note-app:ver-${BUILD_ID} ${FULL_IMAGE}'
                
                sh 'docker push ${FULL_IMAGE}'
            }
        }
        
        stage('Update ECS Service') {
            steps {
                sh '''
                    # Lấy định nghĩa task hiện tại
                    TASK_DEFINITION=$(aws ecs describe-task-definition --task-definition ${TASK_FAMILY} --region "ap-southeast-1")
                    
                    # Tạo một định nghĩa task mới bằng cách thay thế URL image
                    NEW_TASK_DEFINITION=$(echo $TASK_DEFINITION | jq --arg IMAGE "${FULL_IMAGE}" '.taskDefinition | .containerDefinitions[0].image = $IMAGE | del(.taskDefinitionArn) | del(.revision) | del(.status) | del(.requiresAttributes) | del(.compatibilities) | del(.registeredAt) | del(.registeredBy)')
                    
                    # Đăng ký định nghĩa task mới và lấy về revision mới
                    NEW_TASK_INFO=$(aws ecs register-task-definition --region "ap-southeast-1" --cli-input-json "$NEW_TASK_DEFINITION")
                    NEW_REVISION=$(echo $NEW_TASK_INFO | jq '.taskDefinition.revision')
                    
                    # ✅ SỬA LẠI TÊN CLUSTER VÀ SERVICE CHO ĐÚNG
                    aws ecs update-service --cluster taking-note-app-ecs-cluster \\
                                           --service taking-note-app-ecs-service \\
                                           --task-definition ${TASK_FAMILY}:${NEW_REVISION} \\
                                           --force-new-deployment
                '''
            }
        }
    }
}