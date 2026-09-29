// 第9章「通知連携」のスタブ実装。実際に Slack へ送信する場合は
// Slack Notification プラグインが提供する slackSend を呼び出す。
def call(Map args = [:]) {
    def channel = args.channel ?: '#ci-alerts'
    def status = args.status ?: currentBuild.currentResult

    echo "[stub] Slack へ通知: channel=${channel}, status=${status}, " +
        "job=${env.JOB_NAME} #${env.BUILD_NUMBER} (${env.BUILD_URL})"
}
