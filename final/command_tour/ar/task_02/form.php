<?php

    if(empty($_POST)){
        exit();
    }
    require_once "PDO_connect.php";

    $name = trim(strip_tags($_POST["name"]));
    $phone = trim(strip_tags($_POST["phone"]));
    if(!empty($name) and !empty($phone)){
        check_prev_rows($pdo);
        $group_id = (int)get_max_group_id($pdo) + 1;
        insert_row_groups($pdo, $name, $phone, $group_id);
        echo $group_id;
    }
    else{
        echo "error";
    }
?>