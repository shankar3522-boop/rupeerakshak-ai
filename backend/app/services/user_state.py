class UserStateManager:
    def __init__(self):
        # Initialize the user state machine
        self.user_states = {}

    def register_user(self, user_id):
        # Track registration status
        self.user_states[user_id] = {
            'registered': True,
            'wallet_balance': 0.0,
            'intent_classification': None,
            'conversation_stage': 'start'
        }

    def update_wallet_balance(self, user_id, amount):
        # Update wallet balance
        if user_id in self.user_states:
            self.user_states[user_id]['wallet_balance'] += amount

    def classify_intent(self, user_id, intent):
        # Track intent classification
        if user_id in self.user_states:
            self.user_states[user_id]['intent_classification'] = intent

    def update_conversation_stage(self, user_id, stage):
        # Update conversation stage
        if user_id in self.user_states:
            self.user_states[user_id]['conversation_stage'] = stage

    def get_user_state(self, user_id):
        # Get user state
        return self.user_states.get(user_id, None)