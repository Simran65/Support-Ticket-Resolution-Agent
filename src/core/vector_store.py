# Simple knowledge base without vector embeddings to avoid dependency issues
# This is a lightweight implementation for demonstration purposes

class SimpleKnowledgeBase:
    def __init__(self):
        self.documents = {
            "Billing": [
                "Payment processing: Most transactions are processed within 2-3 business days. If you see a pending charge, it will be finalized within 48 hours.",
                "Refund policy: Refunds are processed within 5-7 business days and will appear on your statement within 1-2 billing cycles.",
                "Failed payments: If your payment fails, please verify your card details, ensure sufficient funds, and try again. Contact your bank if issues persist.",
                "Subscription billing: Monthly subscriptions are charged on the same date each month. You can cancel anytime from your account settings."
            ],
            "Technical": [
                "Login troubleshooting: Clear your browser cache, disable browser extensions, and ensure cookies are enabled. Try incognito mode if issues persist.",
                "App crashes: Force close the app, restart your device, and ensure you have the latest version installed from the app store.",
                "Performance issues: Close unnecessary apps, restart your device, and check for available storage space. Update to the latest version if available.",
                "Error codes: Most error codes can be resolved by refreshing the page or restarting the application. Contact support if errors persist."
            ],
            "Security": [
                "Account security: Enable two-factor authentication, use a strong unique password, and never share your login credentials with anyone.",
                "Suspicious activity: If you notice unusual account activity, change your password immediately and contact our security team. Monitor your account for unauthorized changes.",
                "Password reset: Use the 'Forgot Password' link on the login page. You'll receive a reset link via email within 10 minutes.",
                "Data protection: Your personal information is encrypted and stored securely. We never share your data with third parties without consent."
            ],
            "General": [
                "Customer support: Our support team is available 24/7 via live chat, email, or phone. Response time is typically under 2 hours.",
                "Feature requests: We welcome feedback and feature suggestions. Submit your ideas through the feedback form in your account settings.",
                "Account management: Update your profile, preferences, and billing information through your account dashboard. All changes are applied immediately.",
                "Documentation: Comprehensive guides and tutorials are available in our help center. Search by topic or browse categories for detailed information."
            ]
        }
    
    def similarity_search(self, query, k=2, filter=None):
        """Simple similarity search that returns documents based on category filter"""
        category = filter.get("category", "General") if filter else "General"
        
        # Return mock document objects
        class MockDoc:
            def __init__(self, content):
                self.page_content = content
        
        # Return up to k documents from the specified category
        docs = self.documents.get(category, self.documents["General"])
        return [MockDoc(doc) for doc in docs[:k]]

# Create the vector store instance
vector_store = SimpleKnowledgeBase()