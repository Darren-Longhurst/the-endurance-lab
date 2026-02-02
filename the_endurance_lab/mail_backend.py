from django.core.mail.backends.smtp import EmailBackend
import ssl

class ImprovedEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(self.host, self.port, timeout=self.timeout)
            if self.use_tls:
                # This is the fix: calling starttls WITHOUT the problematic arguments
                self.connection.starttls()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise
            return False
