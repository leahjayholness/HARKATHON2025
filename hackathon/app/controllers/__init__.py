def register_controllers(app):
    """
    Register all controllers (blueprints) with the Flask app.
    """
    from app.controllers.authentication_controller import auth_bp
    from app.controllers.homepage_controller import homepage_bp
    from app.controllers.account_controller import account_bp
    from app.controllers.appointment_controller import appointment_bp
    from app.controllers.report_controller import report_bp
    from app.controllers.notice_controller import notice_bp
    from app.controllers.notification_controller import notification_bp
    from app.controllers.timer_controller import timer_bp

    # Register blueprints
    app.register_blueprint(homepage_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(account_bp, url_prefix="/accounts")
    app.register_blueprint(appointment_bp, url_prefix="/appointments")
    app.register_blueprint(report_bp, url_prefix="/reports")
    app.register_blueprint(notice_bp, url_prefix="/notices")
    app.register_blueprint(notification_bp, url_prefix="/notifications")
    app.register_blueprint(timer_bp, url_prefix="/timers")

    app.add_url_rule('/', endpoint='index')