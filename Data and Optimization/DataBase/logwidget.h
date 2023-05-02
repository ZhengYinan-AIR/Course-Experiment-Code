#ifndef LOGWIDGET_H
#define LOGWIDGET_H

#include <QDialog>
#include <QMessageBox>
#include <QJsonDocument>
#include <QFile>
#include <QDebug>
#include <QJsonObject>
#include <QByteArray>
#include <QPainter>

extern bool is_student; //0 teacher
extern QString Q;
extern QString Q1;
namespace Ui {
class LogWidget;
}

class LogWidget : public QDialog
{
    Q_OBJECT

public:
    explicit LogWidget(QWidget *parent = nullptr);
    ~LogWidget();


    void form_init(); //格式初始化
    void func_init(); //功能初始化
    void read_json();
    void write_json();
    void message_init(QString flag1,QString flag2);


signals:
    void login(); //登录主界面信号
    void close_window();  //关闭登录界面信号

public slots:
    void btn_clear_clicked();  //重置按钮按下后触发的事件
    void btn_log_clicked();  //登录按钮按下后触发的事件


private:
    Ui::LogWidget *ui;

    QVector<QVector<double>> Sno={{
        20191001498,
        20191001237,
        20191001356,
        20191002489,
        20191002567,
        20191004652,
        20191004331,
        20191004235,
        20191005356,
        20191005237,
        20181001456,
        20181001489,
        20181001198,
        20181001756,
        20181001156,
        20181001258,
        20181001378,
        20201001498,
        20201001268,},{1498,1237,1356,2489,2567,4652,4331,4235,5356,5237,1456,1489,1198,1756,1156,1258,1378,1498,1268}
    };
    double Tno[2][5]={{1005001,1005016,1005026,1005028,1005037},{5001,5016,5027,5028,5037}};



};

#endif // LOGWIDGET_H
