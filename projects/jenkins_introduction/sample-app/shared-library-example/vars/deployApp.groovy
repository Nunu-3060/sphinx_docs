// 「Jenkins & Jenkins Pipeline 入門」第8章に対応するカスタムステップ。
// Jenkinsfile からは deployApp('production') のように呼び出せる。
def call(String targetEnv) {
    echo "Deploying to ${targetEnv}..."
    sh "./deploy.sh ${targetEnv}"
}
