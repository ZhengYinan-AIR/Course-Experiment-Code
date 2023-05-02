#include "addmessage.h"
#include "ui_addmessage.h"
QString sno;
QString sname;
QString ssex;
int sage;
bool finish1 = 0 ;

QString cno;
QString cname;
QString cpno;
int ccredit;
bool finish2 = 0 ;

QString cno1;
QString sno1;
int grade;
bool finish3 = 0 ;
AddMessage::AddMessage(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::AddMessage)
{
    ui->setupUi(this);
}

AddMessage::~AddMessage()
{
    delete ui;
}

void AddMessage::on_btn_clear_clicked()
{
    this->hide();
}

void AddMessage::on_pushButton_clicked()
{
    ui->stackedWidget->setCurrentIndex(0);
    addmode = 0;

}


void AddMessage::on_pushButton_2_clicked()
{
    ui->stackedWidget->setCurrentIndex(1);
    addmode = 1;

}


void AddMessage::on_pushButton_3_clicked()
{
    ui->stackedWidget->setCurrentIndex(2);
    addmode =2;
}


void AddMessage::on_btn_log_clicked()
{
    if(addmode==0)
    {
        sno=ui->Sno_3->text();
        sname=ui->Sname_3->text();
        ssex=ui->Ssex_3->text();
        QString sage1=ui->lineEdit_3->text();
        sage=sage1.toInt();
        finish1=1;
        this->hide();
    }
    else if(addmode==1)
    {
        cno=ui->cno->text();
        cname=ui->cname->text();
        cpno=ui->cpno->text();
        QString ccredit1=ui->ccredit->text();
        ccredit=ccredit1.toInt();
        finish2=1;
        this->hide();
    }
    else if(addmode==2)
    {
        sno1=ui->sno1->text();
        cno1=ui->cno1->text();
        QString grade1=ui->grade1->text();
        grade=grade1.toInt();
        finish3=1;
        this->hide();
    }
    else
        return;
}

