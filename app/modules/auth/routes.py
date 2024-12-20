from flask import render_template, redirect, url_for, request, current_app, flash
from flask_login import current_user, logout_user

from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from flask_mail import Message

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()


@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        if not authentication_service.is_email_available(email):
            return render_template("auth/signup_form.html", form=form, error=f'Email {email} in use')

        try:
            user = authentication_service.create_with_profile(**form.data, is_confirmed=False)
        except Exception as exc:
            return render_template("auth/signup_form.html", form=form, error=f'Error creating user: {exc}')

        # Create token
        token = authentication_service.generate_confirmation_token(user.id)
        # Create the confirmation URL
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)

        # Create the email message
        msg = Message(
            subject='Verifique su correo',
            recipients=[user.email],
            body=f'Por favor, haga clic en el siguiente enlace para verificar su correo: {confirm_url}'
        )

        # Send the email
        current_app.extensions['mail'].send(msg)

        # Flash the message
        flash('Please, check your email to verify your account!', 'info')

        # Redirect to login
        return redirect(url_for('auth.login'))

    return render_template("auth/signup_form.html", form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        login_status = authentication_service.login(form.email.data, form.password.data)

        # If login is successful
        if login_status == "success":
            return redirect(url_for('public.index'))

        # If the email is not verified
        elif login_status == "email_not_confirmed":
            return render_template("auth/login_form.html", form=form, error='Verify your email')

        # If the credentials are not correct
        elif login_status == "invalid_credentials":
            return render_template("auth/login_form.html", form=form, error='Invalid credentials')

    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@auth_bp.route('/confirm/<token>')
def confirm_email(token):

    user_id = authentication_service.confirm_token(token)
    print(user_id)
    if not user_id:
        logout_user()
        # Flash the message
        flash('Failed verification, check your email!!', 'danger')
        return redirect(url_for('public.index'))

    authentication_service.update_email_confirmed(user_id)

    # Flash the message
    flash('Your account has been verified!', 'success')
    return redirect(url_for('auth.login'))
