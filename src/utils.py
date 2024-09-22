from logging import basicConfig, getLogger, INFO
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


def read_file(file_path: str) -> list:
    """
    Reads file, each content on a new line.

    Args:
        file_path (str): Path to the file containing contents.

    Returns:
        list: A list of contents.
    """
    try:
        with open(file_path, 'r') as file:
            content = [line.strip() for line in file if line.strip()]
        return content
    except Exception as e:
        logger.error(f"Error reading product IDs from file: {e}")
        return []

class EmailAlert:
    def __init__(self, smtp_server, port, sender_email, receiver_email, username, password):
        """
        Initializes the EmailAlert class with SMTP details and email credentials.
        
        Args:
            smtp_server (str): SMTP server address.
            port (int): Port number.
            sender_email (str): Email address of the sender.
            receiver_email (str): Email address of the receiver.
            username (str): Username for SMTP authentication.
            password (str): Password for SMTP authentication.
        """
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.username = username
        self.password = password

    def send_email(self, message, subject='Digi Product Viewer Alert'):
        """
        Sends an email alert with the provided message and subject.

        Args:
            message (str): Body of the email.
            subject (str): Subject of the email (default is 'Digi Product Viewer Alert').
        """
        try:
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            # Send the email
            with SMTP(self.smtp_server, self.port) as server:
                server.starttls()  # Secure the connection
                server.login(self.username, self.password)
                server.sendmail(self.sender_email, self.receiver_email, msg.as_string())

            logger.info(f"Alert email sent to {self.receiver_email}")

        except Exception as e:
            logger.error(f"Failed to send alert email: {e}")
