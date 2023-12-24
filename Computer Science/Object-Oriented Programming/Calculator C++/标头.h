void Calculator::on_Botton_0_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "0";
    if (Inputnum == "0") {
        ui->label->setText(temp);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_1_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "1";
    if (Inputnum == "0") {
        Inputnum = temp;
        ui->label->setText(Inputnum);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_2_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "2";
    if (Inputnum == "0") {
        Inputnum = temp;
        ui->label->setText(Inputnum);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_3_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "3";
    if (Inputnum == "0") {
        Inputnum = temp;
        ui->label->setText(Inputnum);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_4_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "4";
    if (Inputnum == "0") {
        Inputnum = temp;
        ui->label->setText(Inputnum);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_5_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "5";
    if (Inputnum == "0") {
        Inputnum = temp;
        ui->label->setText(Inputnum);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_6_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "6";
    if (Inputnum == "0") {
        Inputnum = temp;
        ui->label->setText(Inputnum);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_7_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "7";
    if (Inputnum == "0") {
        Inputnum = temp;
        ui->label->setText(Inputnum);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_8_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "8";
    if (Inputnum == "0") {
        Inputnum = temp;
        ui->label->setText(Inputnum);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_9_clicked()
{
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    QString temp = "9";
    if (Inputnum == "0") {
        Inputnum = temp;
        ui->label->setText(Inputnum);
    }
    else {
        Inputnum += temp;
        ui->label->setText(Inputnum);
    }
}


void Calculator::on_Botton_point_clicked()
{
    QString temp;
    if (afequ_num == 1) {
        ui->expression->setText(Inputexp);
        afequ_num = 0;
    }
    if (Inputnum.isEmpty() == 1)
        temp = "0.";
    else
        temp = ".";
    Inputnum += temp;
    ui->label->setText(Inputnum);
}


void Calculator::on_Botton_neg_pos_clicked()
{
    QString rhs;
    if (Inputnum == "0") {
        ui->label->setText(Inputnum);
    }
    else {
        string inputnum = Inputnum.toStdString();
        string::iterator it = inputnum.begin();
        double number = stod(inputnum);
        if (number < 0) {
            inputnum.erase(it);
            rhs = QString::fromStdString(inputnum);
            Inputnum = rhs;
        }
        else {
            inputnum = "-" + inputnum;
            rhs = QString::fromStdString(inputnum);
            Inputnum = QString::fromStdString(inputnum);
            Inputnum = "(" + Inputnum + ")";
        }
        ui->label->setText(rhs);
    }
}


void Calculator::on_Botton_equ_clicked()
{
    Inputexp += Inputnum;
    Inputexp += "=";
    ui->expression->setText(Inputexp);
    string inputexp = Inputexp.toStdString();
    ans = doIt(inputexp);
    Inputnum = get_form(ans);
    ui->label->setText(Inputnum);
    Inputexp = QString();
    afequ_num = 1;
    Inputnum = QString();
}


void Calculator::on_Botton_plus_clicked()
{
    if (afequ_num == 0) {
        Inputexp += Inputnum; //将最新的数存入表达式
        Inputexp += "=";    //完整表达式用于下一步计算
        string inputexp = Inputexp.toStdString();
        ans = doIt(inputexp);
        Inputnum = get_form(ans);
        ui->label->setText(Inputnum);
        Inputnum += "+";     //根据不同运算符进行计算
        Inputexp = Inputnum;
        ui->expression->setText(Inputexp);
        Inputnum = QString();
    }
    else {
        Inputexp = get_form(ans);
        Inputexp += "+";
        ui->expression->setText(Inputexp);
    }
}


void Calculator::on_Botton_minus_clicked()
{
    if (afequ_num == 0) {
        Inputexp += Inputnum; //将最新的数存入表达式
        Inputexp += "=";    //完整表达式用于下一步计算
        string inputexp = Inputexp.toStdString();
        ans = doIt(inputexp);
        Inputnum = get_form(ans);
        ui->label->setText(Inputnum);
        Inputnum += "-";     //根据不同运算符进行计算
        Inputexp = Inputnum;
        ui->expression->setText(Inputexp);
        Inputnum = QString();
    }
    else {
        Inputexp = get_form(ans);
        Inputexp += "-";
        ui->expression->setText(Inputexp);
    }
}


void Calculator::on_Botton_multi_clicked()
{
    if (afequ_num == 0) {
        Inputexp += Inputnum; //将最新的数存入表达式
        Inputexp += "=";    //完整表达式用于下一步计算
        string inputexp = Inputexp.toStdString();
        ans = doIt(inputexp);
        Inputnum = get_form(ans);
        ui->label->setText(Inputnum);
        Inputnum += "*";     //根据不同运算符进行计算
        Inputexp = Inputnum;
        ui->expression->setText(Inputexp);
        Inputnum = QString();
    }
    else {
        Inputexp = get_form(ans);
        Inputexp += "*";
        ui->expression->setText(Inputexp);
    }

}


void Calculator::on_Botton_division_clicked()
{
    if (afequ_num == 0) {
        Inputexp += Inputnum; //将最新的数存入表达式
        Inputexp += "=";    //完整表达式用于下一步计算
        string inputexp = Inputexp.toStdString();
        ans = doIt(inputexp);
        Inputnum = get_form(ans);
        ui->label->setText(Inputnum);
        Inputnum += "/";     //根据不同运算符进行计算
        Inputexp = Inputnum;
        ui->expression->setText(Inputexp);
        Inputnum = QString();
    }
    else {
        Inputexp = get_form(ans);
        Inputexp += "*";
        ui->expression->setText(Inputexp);
    }
}


void Calculator::on_Botton_mod_clicked()
{
    if (afequ_num == 0) {
        Inputexp += Inputnum; //将最新的数存入表达式
        Inputexp += "=";    //完整表达式用于下一步计算
        string inputexp = Inputexp.toStdString();
        ans = doIt(inputexp);
        Inputnum = get_form(ans);
        ui->label->setText(Inputnum);
        Inputnum += "%";     //根据不同运算符进行计算
        Inputexp = Inputnum;
        ui->expression->setText(Inputexp);
        Inputnum = QString();
    }
    else {
        Inputexp = get_form(ans);
        Inputexp += "%";
        ui->expression->setText(Inputexp);
    }

}


void Calculator::on_Botton_squar_clicked()  //是一种不存入ans的操作
{
    if (afequ_num == 1) {

    }
    else {
        string inputnum = Inputnum.toStdString();
        double number = stod(inputnum);
        number = pow(number, 2);
        Inputnum = get_form(number);
        ui->label->setText(Inputnum);
        Inputnum = "(" + QString::fromStdString(inputnum) + "^2)";
        Inputexp += Inputnum;
        ui->expression->setText(Inputexp);
        Inputnum = QString();
    }
}


void Calculator::on_Botton_recip_clicked()
{
    string inputnum = Inputnum.toStdString();
    double number = stod(inputnum);
    number = 1 / number;
    Inputnum = get_form(number);
    ui->label->setText(Inputnum);
    Inputnum = "(1/" + QString::fromStdString(inputnum);
    Inputexp += Inputnum;
    ui->expression->setText(Inputexp);
    Inputnum = QString();

}


void Calculator::on_Botton_sqrt_clicked()
{
    string inputnum = Inputnum.toStdString();
    double number = stod(inputnum);
    number = sqrt(number);
    Inputnum = get_form(number);
    ui->label->setText(Inputnum);
    Inputnum = "sqrt(" + QString::fromStdString(inputnum) + ")";
    Inputexp += Inputnum;
    ui->expression->setText(Inputexp);
    Inputnum = QString();

}


void Calculator::on_Botton_c_clicked()
{
    ans = 0;
    Inputnum = "0";
    Inputexp = QString();
    ui->expression->setText(Inputexp);
    ui->label->setText(Inputnum);
}


void Calculator::on_Botton_ce_clicked()
{
    Inputnum = "0";
    ui->label->setText(Inputnum);
}


void Calculator::on_Botton_del_clicked()
{
    Inputnum = Inputnum.left(Inputnum.length() - 1);
    if (Inputnum.isEmpty())
        Inputnum = "0";
    ui->label->setText(Inputnum);
}
