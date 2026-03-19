class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Register all the 'slots' associated with signals from the view
        self.view.login_requested.connect(self.check_login)
        self.view.register_requested.connect(self.add_new_user)

    def check_login(self, username, password):
        user = self.model.verify_credentials(username, password)
        if user is not None:

            # Display a succes message
            self.view.show_success(f"{username} is logged in!")
        else:
            self.view.show_failed(f"{username} is not logged in!")

    def add_new_user(self, username, password):
    
        if self.model.add_user(username, password) is not None:
            # Display a succes message
            self.view.show_success(f"{username} was added!")
        else:
            self.view.show_failed(f"{username} already exists!")
