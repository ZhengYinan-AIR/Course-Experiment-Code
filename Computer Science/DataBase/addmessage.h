#ifndef ADDMESSAGE_H
#define ADDMESSAGE_H

#include <QDialog>

extern QString sno;
extern QString sname;
extern QString ssex;
extern int sage;
extern bool finish1;

extern QString cno;
extern QString cname;
extern QString cpno;
extern int ccredit;
extern bool finish2;

extern QString sno1;
extern QString cno1;
extern int grade;
extern bool finish3;
namespace Ui {
class AddMessage;
}

class AddMessage : public QDialog
{
    Q_OBJECT

public:
    explicit AddMessage(QWidget *parent = nullptr);
    ~AddMessage();

private slots:
    void on_btn_clear_clicked();
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

    void on_btn_log_clicked();

private:
    Ui::AddMessage *ui;
    int addmode = 0;

};

#endif // ADDMESSAGE_H
