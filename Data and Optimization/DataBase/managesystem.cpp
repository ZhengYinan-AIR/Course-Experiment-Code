#include "managesystem.h"
#include "ui_managesystem.h"

int addmode = 0;

ManageSystem::ManageSystem(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::ManageSystem)
{
    ui->setupUi(this);
    // 通过指针创建登录界面类的对象
    m_log = new LogWidget;
    // 调用登录窗口的show()函数显示登录界面
    m_log->show();

    // 建立信号槽，到接收到登录界面发来的login()信号后，调用主窗口的show()函数。
    connect(m_log,SIGNAL(login()),this,SLOT(show()));


    studentqrModel=new QSqlQueryModel(this);
    if(is_student==0){ui->one->setEnabled(true);
        ui->two->setEnabled(true);
        ui->three->setEnabled(true);
        ui->savebutton->setEnabled(true);
        ui->backbutton->setEnabled(true);}
    else if(is_student){ui->one->setEnabled(true);
    }
    myconnect();

    QSqlQuery qr;
    qr.exec("select * from home");
    studentqrModel->setQuery(qr);


    homeModel=new QSqlTableModel(this);
}

bool ManageSystem::myconnect()
{
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("student.db");
    if (!db.open()) {
        QMessageBox::critical(nullptr, QObject::tr("Cannot open database"),
            QObject::tr("Unable to establish a database connection.\n"
                        "This example needs SQLite support. Please read "
                        "the Qt SQL driver documentation for information how "
                        "to build it.\n\n"
                        "Click Cancel to exit."), QMessageBox::Cancel);
        return false;
}
    return true;
}

ManageSystem::~ManageSystem()
{
    delete ui;
}


void ManageSystem::on_one_clicked()
{
    if(is_student==0){
        addmode=0;
        ui->stackedWidget->setCurrentIndex(0);
        homeModel->setHeaderData(0, Qt::Horizontal, QObject::tr("学号"));
        homeModel->setHeaderData(1, Qt::Horizontal, QObject::tr("姓名"));
        homeModel->setHeaderData(2, Qt::Horizontal, QObject::tr("性别"));
        homeModel->setHeaderData(3, Qt::Horizontal, QObject::tr("年龄"));
        homeModel->setTable("student");
        homeModel->setEditStrategy(QSqlTableModel::OnManualSubmit);
        homeModel->select();
        ui->tableView->setModel(homeModel);
    }
    else
    {
        ui->stackedWidget->setCurrentIndex(0);
        QString sql1;
        sql1 = "select student.sno as 学号,student.sname as 姓名,student.ssex as 性别,student.sage as 年龄,cname as 课程名,grade as 成绩 from student,sc,course where student.sno = '"+Q+"' and sc.sno = student.sno and sc.cno = course.cno" ;
        QSqlQueryModel *studentqrmodel=new QSqlQueryModel;
        studentqrmodel->setQuery(sql1);
        ui->tableView->setModel(studentqrmodel);
    }
}


void ManageSystem::on_two_clicked()
{
    if(is_student==0)
    {
        addmode=1;
        ui->stackedWidget->setCurrentIndex(1);
        homeModel->setTable("course");
        homeModel->setEditStrategy(QSqlTableModel::OnManualSubmit);
        homeModel->select();
        homeModel->setHeaderData(0, Qt::Horizontal, QObject::tr("课程号"));
        homeModel->setHeaderData(1, Qt::Horizontal, QObject::tr("课程名"));
        homeModel->setHeaderData(2, Qt::Horizontal, QObject::tr("先行课程号"));
        homeModel->setHeaderData(3, Qt::Horizontal, QObject::tr("学分"));
        ui->tableView_2->setModel(homeModel);
        ui->tableView_2->setItemDelegate(new QSqlRelationalDelegate(ui->tableView_2));
    }
}


void ManageSystem::on_three_clicked()
{
    if(is_student==0)
    {
        addmode=2;
        ui->stackedWidget->setCurrentIndex(2);
        homeModel->setTable("sc");
        homeModel->setEditStrategy(QSqlTableModel::OnManualSubmit);
        homeModel->select();
        homeModel->setHeaderData(0, Qt::Horizontal, QObject::tr("学号"));
        homeModel->setHeaderData(1, Qt::Horizontal, QObject::tr("课程名"));
        homeModel->setHeaderData(2, Qt::Horizontal, QObject::tr("成绩"));
        ui->tableView_3->setModel(homeModel);
        ui->tableView_3->setItemDelegate(new QSqlRelationalDelegate(ui->tableView_3));
    }
}


void ManageSystem::on_addbutton_clicked()
{
    if(is_student==0)
    {
        addview = new AddMessage(this);
        addview->setModal(false);
        addview->show();
        add_delete = 1;
    }
    else
        return;
}


void ManageSystem::on_savebutton_2_clicked()
{
    if(finish1 && is_student==0)
    {
        if(add_delete){
            ui->stackedWidget->setCurrentIndex(0);
            addmode=0;
            QSqlQuery sql;
            qDebug()<<Q;
            QString sql1;
            double sno_int=sno.toDouble();
            if(sno_int>20161000000 && (ssex == "男" || ssex == "女")){
            sql.prepare("INSERT INTO student VALUES (?, ?, ?, ?)");
            sql.bindValue(0, sno);
            sql.bindValue(1, sname);
            sql.bindValue(2, ssex);
            sql.bindValue(3,sage);
            sql.exec();
            QSqlQueryModel *studentqrmodel=new QSqlQueryModel;
            studentqrmodel->setQuery(sql);
            ui->tableView->setModel(studentqrmodel);
            }
            else {

                QMessageBox::about(NULL,"提示","输入有误！ 请重新输入\n");
                addview->show();
            }

        }
        else if(!add_delete){
            ui->stackedWidget->setCurrentIndex(0);
            addmode=0;
            QSqlQuery sql;
            qDebug()<<Q;
            QString sql1;
            sql.prepare("DELETE FROM student WHERE sno = ?");
            sql.bindValue(0, sno);
            sql.exec();
            QSqlQueryModel *studentqrmodel=new QSqlQueryModel;
            studentqrmodel->setQuery(sql);
            ui->tableView->setModel(studentqrmodel);

        }
        ui->stackedWidget->setCurrentIndex(0);
        homeModel->setTable("student");
        homeModel->setEditStrategy(QSqlTableModel::OnManualSubmit);
        homeModel->select();
        homeModel->setHeaderData(0, Qt::Horizontal, QObject::tr("学号"));
        homeModel->setHeaderData(1, Qt::Horizontal, QObject::tr("姓名"));
        homeModel->setHeaderData(2, Qt::Horizontal, QObject::tr("性别"));
        homeModel->setHeaderData(3, Qt::Horizontal, QObject::tr("年龄"));
        ui->tableView->setModel(homeModel);
        ui->tableView->setItemDelegate(new QSqlRelationalDelegate(ui->tableView));
        finish1=0;
    }
    else if(finish2 && is_student==0)
    {
        if(add_delete){
            ui->stackedWidget->setCurrentIndex(1);
            addmode=1;
            QSqlQuery sql;
            qDebug()<<Q;
            QString sql1;
            sql.prepare("INSERT INTO course VALUES (?, ?, ?, ?)");
            sql.bindValue(0, cno);
            sql.bindValue(1, cname);
            sql.bindValue(2, cpno);
            sql.bindValue(3, ccredit);
            sql.exec();
            QSqlQueryModel *studentqrmodel=new QSqlQueryModel;
            studentqrmodel->setQuery(sql);
            ui->tableView_2->setModel(studentqrmodel);
        }
        else if(!add_delete){
            ui->stackedWidget->setCurrentIndex(1);
            addmode=1;
            QSqlQuery sql;
            qDebug()<<Q;
            QString sql1;
            sql.prepare("DELETE FROM course WHERE cno = ? ");
            sql.bindValue(0, cno);
            sql.exec();
            QSqlQueryModel *studentqrmodel=new QSqlQueryModel;
            studentqrmodel->setQuery(sql);
            ui->tableView_2->setModel(studentqrmodel);
            ui->tableView_2->setItemDelegate(new QSqlRelationalDelegate(ui->tableView_2));
        }
        ui->stackedWidget->setCurrentIndex(1);
        homeModel->setTable("course");
        homeModel->setEditStrategy(QSqlTableModel::OnManualSubmit);
        homeModel->select();
        homeModel->setHeaderData(0, Qt::Horizontal, QObject::tr("课程号"));
        homeModel->setHeaderData(1, Qt::Horizontal, QObject::tr("课程名"));
        homeModel->setHeaderData(2, Qt::Horizontal, QObject::tr("先行课程号"));
        homeModel->setHeaderData(3, Qt::Horizontal, QObject::tr("学分"));
        ui->tableView_2->setModel(homeModel);
        finish2=0;
    }
    else if(finish3 && is_student==0)
    {
        if(add_delete){
            ui->stackedWidget->setCurrentIndex(2);
            addmode=2;
            QSqlQuery sql;
            qDebug()<<Q;
            QString sql1;
            double sno_int=sno1.toDouble();
            if(sno_int>20161000000){
            sql.prepare("INSERT INTO sc VALUES (?, ?, ?)");
            sql.bindValue(0, sno1);
            sql.bindValue(1, cno1);
            sql.bindValue(2, grade);
            sql.exec();
            QSqlQueryModel *studentqrmodel=new QSqlQueryModel;
            studentqrmodel->setQuery(sql);
            ui->tableView_3->setModel(studentqrmodel);}
            else {

                QMessageBox::about(NULL,"提示","输入有误！ 请重新输入\n");
                addview->show();
            }

        }
        else if(!add_delete){
            ui->stackedWidget->setCurrentIndex(2);
            addmode=2;
            QSqlQuery sql;
            qDebug()<<Q;
            QString sql1;
            sql.prepare("DELETE FROM sc WHERE sno = ? and cno = ?");
            sql.bindValue(0, sno1);
            sql.bindValue(1, cno1);
            sql.exec();
            QSqlQueryModel *studentqrmodel=new QSqlQueryModel;
            studentqrmodel->setQuery(sql);
            ui->tableView_3->setModel(studentqrmodel);
        }
        ui->stackedWidget->setCurrentIndex(2);
        homeModel->setTable("sc");
        homeModel->setEditStrategy(QSqlTableModel::OnManualSubmit);
        homeModel->select();
        homeModel->setHeaderData(0, Qt::Horizontal, QObject::tr("学号"));
        homeModel->setHeaderData(1, Qt::Horizontal, QObject::tr("课程名"));
        homeModel->setHeaderData(2, Qt::Horizontal, QObject::tr("成绩"));
        ui->tableView_3->setModel(homeModel);
        ui->tableView_3->setItemDelegate(new QSqlRelationalDelegate(ui->tableView_3));
        finish3=0;
    }


}


void ManageSystem::on_deletebutton_clicked()
{
    if(is_student==0)
    {
        if(addmode==0)
        {
            QModelIndex i = ui->tableView->currentIndex();
            int row = i.row();
            sno = ui->tableView->model()->index(row,0).data().toString();
            add_delete=0;
            finish1=1;
        }
        else if(addmode==1)
        {
            QModelIndex i = ui->tableView_2->currentIndex();
            int row = i.row();
            cno = ui->tableView_2->model()->index(row,0).data().toString();
            qDebug()<<cno;
            add_delete=0;
            finish2=1;
        }
        else if(addmode == 2)
        {
            QModelIndex i = ui->tableView_3->currentIndex();
            int row = i.row();
            sno1 = ui->tableView_3->model()->index(row,0).data().toString();
            cno1 = ui->tableView_3->model()->index(row,1).data().toString();
            add_delete=0;
            finish3=1;
        }
    }
    else
        return;
}


void ManageSystem::on_savebutton_clicked()
{
    if(is_student==0)
    {
        homeModel->database().transaction();
        if (homeModel->submitAll()) {
            homeModel->database().commit();
        } else {
            homeModel->database().rollback();
            QMessageBox::warning(this, tr("Cached Table"),
                                 tr("The database reported an error: %1")
                                 .arg(homeModel->lastError().text()));
        }
    }
    else
        return;

}


void ManageSystem::on_backbutton_clicked()
{
    if(is_student==0)
        homeModel->revertAll();//撤回模型更改
    else
        return;
}


void ManageSystem::on_btn_clear_clicked()
{
    homeModel->clear();
    m_log->show();
    this->close();
}

