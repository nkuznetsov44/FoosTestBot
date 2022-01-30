create table telegram_user (
    user_id int not null primary key auto_increment,
    first_name varchar(255) null,
    last_name varchar(255) null,
    username varchar(255) null
);

create table answers (
    id int not null primary key auto_increment,
    user_id int not null,
    question varchar(32) not null,
    answer text null,
    answer_time datetime,
    is_correct boolean null,
    foreign key (user_id) references telegram_user(user_id)
);