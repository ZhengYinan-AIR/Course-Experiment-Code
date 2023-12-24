#ifndef MANAGESYSTEM_H
#define MANAGESYSTEM_H

#include <QMainWindow>
#include <logwidget.h>
#include<QSqlDatabase>
#include<QtSql>
#include<QSqlTableModel>
#include<QSqlRelationalTableModel>
#include<QSqlQuery>
#include "addmessage.h"
QT_BEGIN_NAMESPACE
namespace Ui { class ManageSystem; }
QT_END_NAMESPACE

extern int addmode;

class ManageSystem : public QMainWindow
{
    Q_OBJECT

public:
    ManageSystem(QWidget *parent = nullptr);
    ~ManageSystem();

private slots:
    void on_one_clicked();

    void on_two_clicked();

    void on_three_clicked();

    void on_addbutton_clicked();
    void on_savebutton_2_clicked();

    void on_deletebutton_clicked();

    void on_savebutton_clicked();

    void on_backbutton_clicked();

    void on_btn_clear_clicked();

private:
    Ui::ManageSystem *ui;
    LogWidget *m_log;
private:
    bool myconnect();
    QDialog *addview;

    QSqlTableModel *homeModel;
    QSqlRelationalTableModel *studentModel;
    QSqlQueryModel*studentqrModel;

    bool add_delete = 0;
};
#endif // MANAGESYSTEM_H
