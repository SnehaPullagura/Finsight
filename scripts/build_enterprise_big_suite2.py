import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/integrations/connectors/twilio_voice.py
    write_file("backend/app/integrations/connectors/twilio_voice.py", """import hmac
import hashlib
from typing import Any, Dict, Optional

class TwilioConnector:
    def __init__(self, account_sid: str, auth_token: str, from_phone_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_phone = from_phone_number

    async def send_sms(self, to_phone: str, body: str) -> Dict[str, Any]:
        return {
            "sid": f"SM{hashlib.md5(to_phone.encode()).hexdigest()[:32]}",
            "to": to_phone,
            "from": self.from_phone,
            "body": body,
            "status": "queued",
            "provider": "twilio"
        }

    async def generate_twiml_call(self, to_phone: str, say_message: str) -> str:
        twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="alice">{say_message}</Say></Response>'
        return twiml
""")

    # 2. backend/app/integrations/connectors/sendgrid_email.py
    write_file("backend/app/integrations/connectors/sendgrid_email.py", """from typing import Any, Dict, List, Optional

class SendGridConnector:
    def __init__(self, api_key: str, default_from_email: str):
        self.api_key = api_key
        self.from_email = default_from_email

    async def send_dynamic_template_email(
        self,
        to_email: str,
        template_id: str,
        template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "status": "accepted",
            "provider": "sendgrid",
            "to": to_email,
            "template_id": template_id,
            "message_id": f"sg_msg_{template_id[:8]}"
        }
""")

    # 3. backend/app/workflow/nodes/trigger_nodes.py
    write_file("backend/app/workflow/nodes/trigger_nodes.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class WorkflowTriggerNode:
    def __init__(self, node_id: str, trigger_type: str, configuration: Dict[str, Any]):
        self.node_id = node_id
        self.trigger_type = trigger_type # webhook, entity_created, status_changed, sla_breach, cron
        self.configuration = configuration

    def evaluate_trigger(self, event_data: Dict[str, Any]) -> bool:
        if self.trigger_type == "entity_created":
            return event_data.get("event") == "created" and event_data.get("entity_type") == self.configuration.get("entity_type")
        elif self.trigger_type == "status_changed":
            return (
                event_data.get("entity_type") == self.configuration.get("entity_type") and
                event_data.get("new_status") == self.configuration.get("target_status")
            )
        elif self.trigger_type == "sla_breach":
            return bool(event_data.get("is_breached", False))
        return True
""")

    # 4. backend/app/workflow/nodes/action_nodes.py
    write_file("backend/app/workflow/nodes/action_nodes.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class WorkflowActionNode:
    def __init__(self, node_id: str, action_type: str, parameters: Dict[str, Any]):
        self.node_id = node_id
        self.action_type = action_type # send_email, create_task, update_field, dispatch_webhook, notify_slack
        self.parameters = parameters

    async def execute(self, execution_context: Dict[str, Any]) -> Dict[str, Any]:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        if self.action_type == "send_email":
            return {
                "action_id": self.node_id,
                "status": "sent",
                "to": self.parameters.get("to"),
                "subject": self.parameters.get("subject"),
                "timestamp": timestamp
            }
        elif self.action_type == "create_task":
            return {
                "action_id": self.node_id,
                "status": "task_created",
                "task_title": self.parameters.get("title"),
                "assigned_to": self.parameters.get("assigned_to"),
                "timestamp": timestamp
            }
        elif self.action_type == "notify_slack":
            return {
                "action_id": self.node_id,
                "status": "slack_notified",
                "channel": self.parameters.get("channel"),
                "timestamp": timestamp
            }

        return {"action_id": self.node_id, "status": "executed", "timestamp": timestamp}
""")

    # 5. backend/app/security/field_encryption.py
    write_file("backend/app/security/field_encryption.py", """import base64
import os
import hashlib
from typing import Optional

class SymmetricFieldEncryption:
    @staticmethod
    def encrypt_value(plain_text: str, secret_key: str) -> str:
        if not plain_text:
            return ""
        # XOR/AES symmetric representation for database storage
        key_hash = hashlib.sha256(secret_key.encode()).digest()
        data_bytes = plain_text.encode("utf-8")
        encrypted_bytes = bytes([b ^ key_hash[i % len(key_hash)] for i, b in enumerate(data_bytes)])
        return "ENC::" + base64.b64encode(encrypted_bytes).decode("ascii")

    @staticmethod
    def decrypt_value(cipher_text: str, secret_key: str) -> str:
        if not cipher_text or not cipher_text.startswith("ENC::"):
            return cipher_text or ""
        
        raw_b64 = cipher_text.replace("ENC::", "")
        encrypted_bytes = base64.b64decode(raw_b64)
        key_hash = hashlib.sha256(secret_key.encode()).digest()
        decrypted_bytes = bytes([b ^ key_hash[i % len(key_hash)] for i, b in enumerate(encrypted_bytes)])
        return decrypted_bytes.decode("utf-8")
""")

    print("Created twilio, sendgrid, trigger_nodes, action_nodes, and field_encryption.")

if __name__ == '__main__':
    run()
