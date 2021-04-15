from flask import render_template, url_for, session, redirect, flash, request
from forms import SignInForm, RegisterForm, PostForm
from app import app, UserModel, PostsModel
from general_crud import create, update, delete
from werkzeug.utils import secure_filename
from datetime import date


pages_nav_list = [
    ("list_posts", "პოსტები"),
    ("list_people", "ხალხი"),
    ("list_pages", "გვერდები"),
    ("auth", "შესვლა")
]


@app.route('/timeline', methods=['GET', 'POST'])
def list_posts():
    user = None
    form_post = PostForm()
    all_posts = PostsModel.query.all()
    authors = UserModel.query.all()

    try:
        if session['username']:
            user = UserModel.query.filter_by(username=session['username']).first()
            print('27')
            if request.method == 'POST':
                if form_post.text.data is None and form_post.media.data is None:
                    print(30)
                    pass
                else:
                    print(33)
                    text = form_post.text.data
                    print(35)
                    media = form_post.media.data
                    print(37)
                    time = '04/14/2021'
                    print(39)
                    if media:
                        print(41)
                        media_title = secure_filename(f'{user.username}_{media.filename}')
                        print(43, media_title)
                        media.save(f'static/post_uploads/{media_title}')
                    else:
                        media_title = None
                    print(45)
                    print(media)
                    print('everything: ', text)
                    print(media)
                    print(time)
                    print(user.id)
                    received_data = (time, text, media_title, user.id)
                    print(received_data)
                    create(received_data, PostsModel)
                    print('finish', received_data)

    except:
        pass

    return render_template('posts.html', pages=pages_nav_list, user=user, form=form_post, all_posts=all_posts, authors=authors)


@app.route('/people')
def list_people():
    # viewed shows the number of already viewed people (on previous pages)
    people_list = UserModel.query.all()
    return render_template('people.html', pages=pages_nav_list, people_list=people_list)

# @app.route('/people/<int:viewed>')
# def list_people(viewed=0):
#     # viewed shows the number of already viewed people (on previous pages)
#     return render_template('people.html', pages=pages_nav_list, viewed=viewed)


@app.route('/pages')
def list_pages():
    return render_template('placeholder.html', pages=pages_nav_list)


@app.route('/', methods=['GET', 'POST'])
def auth():
    show_flash = False

    try:
        if session['username'] is not None:  # if already logged in, redirects to user's profile
            pages_nav_list[3] = ("profile", session['username'])
            return redirect('/profile')
    except:
        pass

    form_sign_in = SignInForm()
    form_register = RegisterForm()

    if request.method == 'POST':

        # Login Attempt
        if form_sign_in.validate_on_submit():
            target_account = None
            identifier = form_sign_in.identifier.data.lower()
            login_password = form_sign_in.login_password.data

            # Check if logging in through Email
            if UserModel.query.filter_by(email=identifier).first():
                target_account = UserModel.query.filter_by(email=identifier).first()

            # Check if logging in through Username
            elif UserModel.query.filter_by(username=identifier).first():
                target_account = UserModel.query.filter_by(username=identifier).first()

            #  Check Password only if the account was found either through Email or Username
            if target_account:
                correct_password = target_account.password

                if login_password == correct_password:  # Successful log-in
                    show_flash = True
                    flash('წარმატებით შეხვედით სისტემაში!')

                    # if remember_me was checked make session permanent
                    remember_me = form_sign_in.remember_me.data
                    if remember_me:
                        session.permanent = True
                    else:
                        session.permanent = False

                    session['username'] = target_account.username  # used to determine if logged in
                    pages_nav_list[3] = ("profile", session['username'])
                    return redirect(url_for('profile'))

                else:  # Wrong Password
                    form_sign_in.login_password.data = ''
                    show_flash = True
                    flash('პაროლი არასწორია')

            else:  # Wrong Email or Password
                form_sign_in.login_password.data = ''
                show_flash = True
                flash('ამ მეილით ან იუზერნეიმით მომხმარებელი არ მოიძებნა')

        # Register Attempt
        elif form_register.validate_on_submit():
            success = True
            # initialize received data
            username = form_register.username.data.lower()
            name_first = form_register.name_first.data
            name_last = form_register.name_last.data
            email = form_register.email.data.lower()
            phone = form_register.phone.data
            age = form_register.age.data
            sex = form_register.sex.data
            password = form_register.password.data

            # check if the username and email are unique
            if UserModel.query.filter_by(username=username).first():
                success = False
                show_flash = True
                flash('იუზერნეიმი დაკავებულია')
            elif UserModel.query.filter_by(email=email).first():
                success = False
                show_flash = True
                flash('მეილი დაკავებულია')

            if success:
                # check if picture was uploaded and save it
                picture = form_register.picture.data
                if picture:
                    picture_title = secure_filename(f'{username}_{picture.filename}')
                    picture.save(f'static/profile_pictures/{picture_title}')

                # add everything to DB
                received_data = (username, name_first, name_last, email, phone, age, sex, password, picture_title)
                create(received_data, UserModel)

                # automatically log in
                session['email'] = email  # used to display where a confirmation message would be sent
                session['username'] = username  # used to determine if logged in
                pages_nav_list[3] = ("profile", session['username'])
                show_flash = True
                flash('რეგისტრაცია წარმატებით დასრულდა!')
                return redirect(url_for('success_register'))

        else:  # When data didn't pass WTForms validators
            show_flash = True
            flash('მონაცემები არასწორადაა შეყვანილი. თავიდან სცადეთ. ')

    return render_template('auth.html', pages=pages_nav_list, form_sign_in=form_sign_in, form_register=form_register, show_flash=show_flash)


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/<username>')
def profile(username=None):
    show_flash = True

    if request.method == 'POST':
        form_register = RegisterForm()
        target_user = UserModel.query.filter_by(username=session['username']).first()
        # initialize received data
        username = form_register.username.data
        name_first = form_register.name_first.data
        name_last = form_register.name_last.data
        email = form_register.email.data.lower()
        phone = form_register.phone.data
        age = form_register.age.data
        sex = form_register.sex.data
        password = form_register.password.data
        new_data = []
        count = 0
        for filled in [username, name_first, name_last, email, phone, age, sex, password]:
            print('For loop')
            print(new_data)
            if filled is None:
                print('NONE')
                if count == 0:
                    print(target_user)
                    print(filled, target_user.username)
                    filled = target_user.username
                    print(filled)
                    new_data.append(filled)
                    print(new_data)
                elif count == 1:
                    filled = target_user.name_first
                    new_data.append(filled)
                elif count == 2:
                    filled = target_user.name_last
                    new_data.append(filled)
                elif count == 3:
                    filled = target_user.email
                    new_data.append(filled)
                elif count == 4:
                    filled = target_user.phone
                    new_data.append(filled)
                elif count == 5:
                    filled = target_user.age
                    new_data.append(filled)
                elif count == 6:
                    filled = target_user.sex
                    new_data.append(filled)
                elif count == 7:
                    filled = target_user.password
                    new_data.append(filled)
                count += 1
            else:
                print('FILLED')
                if count == 0:
                    new_data.append(filled)
                elif count == 1:
                    new_data.append(filled)
                elif count == 2:
                    new_data.append(filled)
                elif count == 3:
                    new_data.append(filled)
                elif count == 4:
                    new_data.append(filled)
                elif count == 5:
                    new_data.append(filled)
                elif count == 6:
                    new_data.append(filled)
                elif count == 7:
                    new_data.append(filled)
                count += 1
        print(new_data)
        delete(UserModel, target_user.id)
        create(new_data, UserModel)
        # update(UserModel, username, new_data)
        flash('მონაცემები განახლდა')
        redirect('/profile')

    elif username is None:
        try:
            if session['username'] is None:
                return redirect('/')
        except:
            return redirect('/')
        else:
            user = UserModel.query.filter_by(username=session['username']).first()
            return render_template('my_profile.html', pages=pages_nav_list, show_flash=show_flash, user=user, form_register=RegisterForm())
    else:
        user = UserModel.query.filter_by(username=username).first()
        return render_template('people_profile.html', pages=pages_nav_list, show_flash=show_flash, user=user)


@app.route('/success_register')
def success_register():
    return render_template('success_register.html', pages=pages_nav_list)


@app.route('/logoff')
def logoff():
    session['username'] = None
    pages_nav_list[3] = ("auth", "შესვლა")
    return redirect('/')
