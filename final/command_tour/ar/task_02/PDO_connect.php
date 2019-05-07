<?php

//----Данные для подключения-------------
$db_server = "";
$user = "";
$pass = "";
$db_name = "nti";

try {
    $pdo = new PDO("mysql:host=$db_server;dbname=$db_name", $user, $pass);
} catch (PDOException $e) {
    die($e->getMessage());
}

function insert_row_groups($pdo, $name, $phone, $group_number){
    $sth = $pdo->prepare("INSERT INTO `groups` (`id`, `name`, `phone`, `group_id`, `timestamp`)
                                       VALUES (NULL, :name, :phone, :group_number, CURRENT_TIMESTAMP)");


    $sth->bindParam(':name', $name, PDO::PARAM_STR, 255);
    $sth->bindParam(':phone', $phone, PDO::PARAM_STR, 255);
    $sth->bindParam(':group_number', $group_number, PDO::PARAM_INT, 3);
    $sth->execute();
}

function get_max_group_id($pdo){
    $sth = $pdo->prepare("SELECT MAX(`group_id`) FROM `groups`");
    $sth->execute();
    $row = $sth->fetch();
    return $row[0];
}

function check_prev_rows($pdo){
    $sth = $pdo->prepare("SELECT `timestamp` FROM `groups` LIMIT 1");
    $sth->execute();
    $row = $sth->fetch()[0];
    $date = new DateTime($row);
    $cur_date = new DateTime("now");

    $dteDiff  = $date->diff($cur_date);
    if($dteDiff->days > 0){
        delete_prev_rows($pdo);
    }
}

function delete_prev_rows($pdo){
    $sth = $pdo->prepare("TRUNCATE TABLE `groups`");
    $sth->execute();
}

?>