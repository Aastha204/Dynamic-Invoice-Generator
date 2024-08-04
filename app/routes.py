from flask import Blueprint, render_template, flash, redirect,request,url_for,session
from .forms import LoginForm, SignUpForm, PasswordChangeForm,UserDetailChange,InvoicedetailForm
from .models import User,Subscription,Invoice,template_1,template_2_3
from . import db
from flask_login import login_user, login_required, logout_user,current_user
from datetime import datetime, timedelta


routes = Blueprint('routes', __name__)


@routes.route("/")
def home():
    return render_template('index.html')

@routes.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect('/')
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_user = User()
            new_user.email = email
            new_user.username = username
            new_user.password = password2

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Account Created Successfully, You can now Login')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account Not Created!!, Email already exists')

            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''
        else:
            flash('Passwords do not match')

    return render_template('signup.html', form=form)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            if user.verify_password(password=password):
                login_user(user)
                active_subscription = Subscription.query.filter(Subscription.user_id == current_user.id,Subscription.end_date > datetime.utcnow()).first()
                if not active_subscription:
                    flash("Please Subscribe for generating invoices")
                    return redirect(url_for('routes.subscription'))
                return redirect('/')
            else:
                flash('Incorrect Email or Password')

        else:
            flash('Account does not exist please Sign Up')

    return render_template('login.html', form=form)


@routes.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')



@routes.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    if user_id != current_user.id:
        return redirect(url_for('routes.home'))  # Redirect if accessing another user's profile
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.city = request.form.get('city')
        user.country = request.form.get('country')
        user.occupation = request.form.get('occupation')

        # Handle subscription update
        subscription = Subscription.query.filter_by(user_id=user_id).first()
        if subscription:
            subscription.plan = request.form.get('subscription_plan')
        else:
            # If no subscription exists, create a new one
            new_subscription = Subscription(
                user_id=user_id,
                category='Freelancer',  # Default category or as per your requirement
                plan=request.form.get('subscription_plan'),
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=30)  # Example: setting 30 days validity
            )
            db.session.add(new_subscription)
        
        db.session.commit()
        return redirect(url_for('profile', user_id=user_id))
    
    subscription = Subscription.query.filter_by(user_id=user_id).first()
    subscription_plan = subscription.plan if subscription else 'Free'

    return render_template('userprofile.html', user=user, subscription_plan=subscription_plan)

@routes.route('/template', methods=['GET'])
def templates():
    return render_template('template.html')

@routes.route('/template/<int:template_id>', methods=['GET'])
def invoice_template(template_id):
    if template_id not in [1, 2, 3]:
        return render_template('404.html')
    image_filename = f'images/template{template_id}.jpg'
    return render_template('invoice_template.html', template_id=template_id, image_filename=image_filename)

@routes.route('/subscription', methods=['GET', 'POST'])
def subscription():
    return render_template('subscription.html')

@routes.route('/subscribe/<plan>/<category>', methods=['POST'])
@login_required
def subscribe(plan, category):
    # Calculate end date based on the plan
    if plan == 'monthly':
        end_date = datetime.utcnow() + timedelta(days=30)
    else:
        end_date = datetime.utcnow() + timedelta(days=365)
    
    new_subscription = Subscription(
        user_id=current_user.id,
        category=category,
        plan=plan,
        start_date=datetime.utcnow(),
        end_date=end_date
    )
    
    db.session.add(new_subscription)
    db.session.commit()
    return redirect(url_for('routes.home')) 



@routes.route('/change-password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    form = PasswordChangeForm()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if user.verify_password(current_password):
            if new_password == confirm_new_password:
                user.password = confirm_new_password
                db.session.commit()
                flash('Password Updated Successfully')
                return redirect(f'/profile/{user.id}')
            else:
                flash('New Passwords do not match!!')

        else:
            flash('Current Password is Incorrect')

    return render_template('change_password.html', form=form)

@routes.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def changeuserdetail(user_id):
    user = User.query.get_or_404(user_id)
    form = UserDetailChange(
        name=user.name,
        city=user.city,
        country=user.country,
        occupation=user.occupation,
        occupation_city=user.occupation_city,
        occupation_country=user.occupation_country
    )

    if form.validate_on_submit():
        user.name = form.name.data
        user.city = form.city.data
        user.country = form.country.data
        user.occupation = form.occupation.data
        user.occupation_city = form.occupation_city.data
        user.occupation_country = form.occupation_country.data
        
        db.session.commit()
        flash('Updated Successfully')
        return redirect(f'/profile/{user.id}')  

    return render_template('change_profile.html', form=form, user_id=user_id)



@routes.route('/use_template/<int:template_id>', methods=['GET', 'POST'])
@login_required
def use_template(template_id):
    # Check if the user has an active subscription
    active_subscription = Subscription.query.filter(
        Subscription.user_id == current_user.id,
        Subscription.end_date > datetime.utcnow()
    ).first()

    if not active_subscription:
        return redirect(url_for('routes.subscription'))

    # Store the template_id in the session
    session['template_id'] = template_id
    
    form = InvoicedetailForm()  # Create an instance of the form
    
    if template_id == 1:
        return render_template('usetemplate.html', form=form)
    elif template_id == 2:
        return render_template('usetemplate.html', form=form)
    elif template_id == 3:
        return render_template('template3.html', form=form)
    else:
        # flash('Invalid template ID.')
        return 'Invalid template'




@routes.route('/draft_invoice', methods=['GET'])
@login_required
def draft_html():
    invoices = Invoice.query.filter_by(user_id=current_user.id, status='draft').all()
    return render_template('draft_invoices.html', invoices=invoices)



@routes.route('/invoice/generate/<int:invoice_id>', methods=['POST'])
@login_required
def generate_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    template_id = invoice.template_id

    if template_id == 1:
        return "template_id is 1"
    elif template_id == 3:
        template = template_2_3.query.filter_by(invoice_id=invoice.id).first()
        form = InvoicedetailForm(
            house_no=invoice.sender_houseno,
            city=invoice.sender_city,
            country=invoice.sender_country,
            email=invoice.sender_email,
            phone_no=invoice.sender_phone,
            due_date=invoice.due_date,
            receiver_name=invoice.receiver_name,
            receiver_email=invoice.receiver_email,
            receiver_phone=invoice.receiver_phone,
            address_line1=invoice.receiver_city,
            address_line2=invoice.receiver_country,
            hours_worked1=template.hours_worked1,
            description1=template.description1,
            rate_per_hour1=template.rate_per_hour1,
            amount1=template.amount1,
            hours_worked2=template.hours_worked2,
            description2=template.description2,
            rate_per_hour2=template.rate_per_hour2,
            amount2=template.amount2,
            hours_worked3=template.hours_worked3,
            description3=template.description3,
            rate_per_hour3=template.rate_per_hour3,
            amount3=template.amount3,
            total_amount=invoice.amount,
            gst=invoice.total_tax,
            grand_total=invoice.sub_total
        )
    return render_template('template3_print.html',form=form, invoice_id=invoice_id)

    # return 'generate invoice'



@routes.route('/invoice/delete/<int:invoice_id>', methods=['POST'])
@login_required
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if invoice.user_id != current_user.id:
        
        return "not authorized"

    # Delete the associated template_2_3 entry if it exists
    template_entry = template_2_3.query.filter_by(invoice_id=invoice.id).first()
    if template_entry:
        db.session.delete(template_entry)
    
    # Delete the invoice
    db.session.delete(invoice)
    db.session.commit()
    
    # flash('Invoice deleted successfully!', 'success')
    return redirect(url_for('routes.draft_html'))

    




@routes.route('/invoice', methods=['GET', 'POST'])
@login_required
def invoice():
    form = InvoicedetailForm()

    if form.validate_on_submit():
        # Retrieve the template_id from the session
        template_id = session.get('template_id')
        if not template_id:
            # flash('Template ID is missing.')
            return 'No template Id'

        # Calculate the total amount, GST, and grand total on the server side
        amount1 = float(form.amount1.data) if form.amount1.data else 0
        amount2 = float(form.amount2.data) if form.amount2.data else 0
        amount3 = float(form.amount3.data) if form.amount3.data else 0

        total_amount = amount1 + amount2 + amount3
        gst = total_amount * 0.03  # 3% GST
        grand_total = total_amount + gst

       

        # Create and save the main invoice details
        new_invoice = Invoice(
            user_id=current_user.id,
            template_id=template_id,
            receiver_name=form.receiver_name.data,
            receiver_email=form.receiver_email.data,
            receiver_phone=form.receiver_phone.data,
            due_date=form.due_date.data,
            receiver_city=form.address_line1.data,
            receiver_country=form.address_line2.data,
            amount=total_amount,
            discount=0,  # Assuming no discount field in form
            total_tax=gst,
            sub_total=grand_total
        )
        db.session.add(new_invoice)
        db.session.commit()

        # Handle and save each work detail item
        new_template_2_3_entry = template_2_3(
            invoice_id=new_invoice.id,
            hours_worked1=form.hours_worked1.data,
            description1=form.description1.data,
            rate_per_hour1=form.rate_per_hour1.data,
            amount1=form.amount1.data,

            hours_worked2=form.hours_worked2.data,
            description2=form.description2.data,
            rate_per_hour2=form.rate_per_hour2.data,
            amount2=form.amount2.data,

            hours_worked3=form.hours_worked3.data,
            description3=form.description3.data,
            rate_per_hour3=form.rate_per_hour3.data,
            amount3=form.amount3.data
        )
        db.session.add(new_template_2_3_entry)
        db.session.commit()

        # Redirect to a success page or a page that displays the generated invoice
        return redirect(url_for('routes.draft_html'))  
  # Make sure 'success_page' route is defined

    return 'not success page' # Make sure the form is rendered in case of errors

@routes.route('/update-invoice/<int:invoice_id>', methods=['GET', 'POST'])
@login_required
def update_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    template_id = invoice.template_id

    if template_id == 1:
        return "template_id is 1"
    elif template_id == 3:
        template = template_2_3.query.filter_by(invoice_id=invoice.id).first()
        form = InvoicedetailForm(
            house_no=invoice.sender_houseno,
            city=invoice.sender_city,
            country=invoice.sender_country,
            email=invoice.sender_email,
            phone_no=invoice.sender_phone,
            due_date=invoice.due_date,
            receiver_name=invoice.receiver_name,
            receiver_email=invoice.receiver_email,
            receiver_phone=invoice.receiver_phone,
            address_line1=invoice.receiver_city,
            address_line2=invoice.receiver_country,
            hours_worked1=template.hours_worked1,
            description1=template.description1,
            rate_per_hour1=template.rate_per_hour1,
            amount1=template.amount1,
            hours_worked2=template.hours_worked2,
            description2=template.description2,
            rate_per_hour2=template.rate_per_hour2,
            amount2=template.amount2,
            hours_worked3=template.hours_worked3,
            description3=template.description3,
            rate_per_hour3=template.rate_per_hour3,
            amount3=template.amount3,
        )

        if form.validate_on_submit():
            amount1 = float(form.amount1.data) if form.amount1.data else 0
            amount2 = float(form.amount2.data) if form.amount2.data else 0
            amount3 = float(form.amount3.data) if form.amount3.data else 0

            total_amount = amount1 + amount2 + amount3
            gst = total_amount * 0.03  # 3% GST
            grand_total = total_amount + gst

            invoice.sender_houseno = form.house_no.data
            invoice.sender_city = form.city.data
            invoice.sender_country = form.country.data
            invoice.sender_email = form.email.data
            invoice.sender_phone = form.phone_no.data
            invoice.due_date = form.due_date.data
            invoice.receiver_name = form.receiver_name.data
            invoice.receiver_email = form.receiver_email.data
            invoice.receiver_phone = form.receiver_phone.data
            invoice.receiver_city = form.address_line1.data
            invoice.receiver_country = form.address_line2.data
            invoice.amount = total_amount
            invoice.discount = 0
            invoice.total_tax = gst
            invoice.sub_total = grand_total

            template.hours_worked1 = form.hours_worked1.data
            template.description1 = form.description1.data
            template.rate_per_hour1 = form.rate_per_hour1.data
            template.amount1 = form.amount1.data
            template.hours_worked2 = form.hours_worked2.data
            template.description2 = form.description2.data
            template.rate_per_hour2 = form.rate_per_hour2.data
            template.amount2 = form.amount2.data
            template.hours_worked3 = form.hours_worked3.data
            template.description3 = form.description3.data
            template.rate_per_hour3 = form.rate_per_hour3.data
            template.amount3 = form.amount3.data

            db.session.commit()
            return redirect(url_for('routes.draft_html'))  # Adjust this to the correct route name

        return render_template('template3_update.html',form=form, invoice_id=invoice_id)

    return 'no update'

