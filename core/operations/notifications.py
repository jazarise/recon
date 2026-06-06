class NotificationManager:
    def send_email(self, recipient: str, subject: str, body: str):
        pass

    def send_slack(self, webhook_url: str, message: str):
        pass

    def notify(self, level: str, message: str):
        # Dispatch logic
        pass
