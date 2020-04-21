
def sitePackageDir = "env/lib/python3.6/site-packages"
node {
    stage('Clean Up'){
        cleanWs()
    }
    stage('Clone'){
        git credentialsId: 'GIT', url: 'https://github.com/jmpcba/MG.git'
    }

    stage('Deploy') {
        echo "####################"
        echo "# UPLOADING TO AWS #"
        echo "####################"  
            withAWS(credentials: 'AWS CREDENTIALS', region: 'us-east-1') {
            s3Upload acl: 'PublicReadWrite', includePathPattern:'**/*', bucket: 'jmpcba-mg-presupuesto', workingDir: 'frontend'
        }
    }
}