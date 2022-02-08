create table telegram_user (
    user_id int not null primary key auto_increment,
    first_name varchar(255) null,
    last_name varchar(255) null,
    username varchar(255) null
);

create table test_session (
    id int not null primary key auto_increment,
    user_id int not null,
    start_time datetime,
    end_time datetime null,
    score int null,
    is_checked boolean,
    foreign key (user_id) references telegram_user(user_id)
);

create table answers (
    id int not null primary key auto_increment,
    test_session_id int not null,
    question varchar(32) not null,
    answer text null,
    is_correct boolean null,
    foreign key (test_session_id) references test_session(id)
);