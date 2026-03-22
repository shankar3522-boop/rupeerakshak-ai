class UserStateManager:
    def __init__(self):
        self.user_states = {}

    def register_user(self, user_id):
        self.user_states[user_id] = {
            'registered': True,
            'wallet_balance': 0.0,
            'intent_classification': None,
            'conversation_stage': 'start'
        }

    def update_wallet_balance(self, user_id, amount):
        if user_id in self.user_states:
            self.user_states[user_id]['wallet_balance'] += amount

    def classify_intent(self, user_id, intent):
        if user_id in self.user_states:
            self.user_states[user_id]['intent_classification'] = intent

    def update_conversation_stage(self, user_id, stage):
        if user_id in self.user_states:
            self.user_states[user_id]['conversation_stage'] = stage

    def get_user_state(self, user_id):
        return self.user_states.get(user_id, None)