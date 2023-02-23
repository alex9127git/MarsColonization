from users import User


def fill_tables(session):
    if len(session.query(User).all()) == 0:
        add_user(session, "Scott", "Ridley", 21, "captain", "research engineer",
                 "module 1", "scott_chief@mars.org", "VerY_5Tr0nG_P@Ssw0Rd")
        add_user(session, "Andy", "Wheel", 23, "officer", "central pilot",
                 "head module", "ma1n_wh33l@mars.org", "tH15_sh0UlD_Be_g0Od")
        add_user(session, "Mark", "Woatney", 35, "officer", "ship builder",
                 "module 3", "m4rk_w0atney@mars.org", "mark343214231")
        add_user(session, "Teddy", "Sanders", 19, "chief", "surgeon",
                 "head module", "t3ddySanders@mars.org", "why_do_i_exist")


def add_user(session, surname, name, age, position, specialty, address, email, password):
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = specialty
    user.address = address
    user.email = email
    user.hashed_password = password
    session.add(user)
    session.commit()
