#ifndef ANALOGCLOCK_H
#define ANALOGCLOCK_H

#include <QDialog>

class AnalogClock : public QDialog
{
    Q_OBJECT

public:
    AnalogClock(QWidget *parent = nullptr);
    ~AnalogClock();
protected:
    void paintEvent(QPaintEvent*) Q_DECL_OVERRIDE;
};
#endif // ANALOGCLOCK_H
