import os
import uuid
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable = False)


    tasks = db.relationship('Task', backref='owner', lazy=True)
    exams = db.relationship('Exam', backref='owner', lazy=True)
    subjects = db.relationship('Subject', backref='owner',lazy=True)

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=True)
    describe = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    #New columns for insights
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Exam(db.Model):
    __tablename__ = 'exam'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=True)
    revision = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    room = db.Column(db.String(50), nullable=True)
    created_at_exam = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at_exam = db.Column(db.DateTime, nullable=True)


    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', use_alter=True, name='fk_exam_owner'),
        nullable=False
    )



class Subject(db.Model):
    __tablename__ = 'Subject'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=True)
    room = db.Column(db.String(50), nullable=True)
    grade = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=True)


    subject_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)