#include "logwidget.h"
#include "ui_logwidget.h"

bool is_student =0;
bool is_teacher =0;
QString Q;
QString Q1;

LogWidget::LogWidget(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::LogWidget)
{
    ui->setupUi(this);
    setWindowTitle("信息门户");
    func_init();
}

LogWidget::~LogWidget()
{
    delete ui;
}


void LogWidget::func_init()
{
    // connect
    // 触发重置按钮的信号槽连接
    connect(ui->btn_clear,SIGNAL(clicked()),this,SLOT(btn_clear_clicked()));
    // 触发登录按钮的信号槽连接
    connect(ui->btn_log,SIGNAL(clicked()),this,SLOT(btn_log_clicked()));
    // 发出信号后关闭登录窗口的信号槽连接
    connect(this,SIGNAL(close_window()),this,SLOT(close()));


    ui->edit_pw->setEchoMode(QLineEdit::Password);//输入的时候就显示圆点


    read_json();
}


// 清理输入栏
void LogWidget::btn_clear_clicked()
{
    ui->edit_pw->clear();
    ui->edit_name->clear();
}




void LogWidget::btn_log_clicked()
{
    bool loginsu = 0;
    Q = ui->edit_name->text();
    Q1 = ui->edit_pw->text();
    double dname = Q.toDouble();
    double dpassword = Q1.toDouble();

    for(int i=0;i<19;i++)
    {
        if(dname==Sno[0][i])
        {
            if(dpassword==Sno[1][i])
            {
                loginsu=1;
                is_student=1;
                break;
            }
        }
        else if(dname == Tno[0][i])
        {
            if(dpassword==Tno[1][i])
            {
                loginsu=1;
                is_student=0;
                break;
            }
        }
    }
    if (loginsu==1)
    {
        emit(login());
        write_json();
        emit(close_window());
    }
    else
        QMessageBox::information(this, "Warning","Username or Password is wrong !");


}


void LogWidget::read_json()
{
    //打开文件
    QFile file(QApplication::applicationDirPath()+"/config.json");
    if(!file.open(QIODevice::ReadOnly)) {
        qDebug() << "File open failed!";
    } else {
        qDebug() <<"File open successfully!";
    }
    QJsonDocument jdc(QJsonDocument::fromJson(file.readAll()));
    QJsonObject obj = jdc.object();
    QString save_name_flag=obj.value("SAVE_NAME").toString();
    QString save_password_flag=obj.value("SAVE_PASSWORD").toString();
    message_init(save_name_flag,save_password_flag);


}


void LogWidget::write_json()
{
    QFile file(QApplication::applicationDirPath()+"/config.json");
    if(!file.open(QIODevice::WriteOnly)) {
        qDebug() << "File open failed!";
    } else {
        qDebug() <<"File open successfully!";
    }
    QJsonObject obj;
    bool flag = ui->check_name->isChecked();
    if(flag == true)
    {
        obj["SAVE_NAME"] = "1";
    }
    else
        obj["SAVE_NAME"] = "0";
    flag = ui->check_pw->isChecked();
    if(flag == true)
    {
        obj["SAVE_PASSWORD"] = "1";
    }
    else
        obj["SAVE_PASSWORD"] = "0";
    QJsonDocument jdoc(obj);
    file.write(jdoc.toJson());
    file.flush();
}



void LogWidget::message_init(QString flag1,QString flag2)
{
    //qDebug() << flag1 << "^^^" << flag2 ;
    if (flag1 == "1")
    {
        ui->edit_name->setText("1005001");
        ui->check_name->setChecked(true);
    }
    if(flag2 == "1")
    {
        ui->edit_pw->setText("5001");
        ui->check_pw->setChecked(true);
    }
}
