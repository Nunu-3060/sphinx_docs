package org.example.pipeline

// src/ 配下の通常の Groovy クラスは、vars/ のグローバル変数と違って
// sh/echo などの Pipeline ステップに暗黙にはアクセスできない。
// そのため、呼び出し元の Pipeline（steps）を明示的に受け取って使う。
class Deployer implements Serializable {
    private final steps

    Deployer(steps) {
        this.steps = steps
    }

    void deployTo(String targetEnv) {
        steps.echo "Deployer: deploying to ${targetEnv}"
        steps.sh "./deploy.sh ${targetEnv}"
    }
}
