<?php
session_start();
if(isset($_POST['submit']))
{
    $temp_file = "temp_owl.owls";
    $target_dir = "docs/";
    $target_file = $target_dir . basename($_FILES['owl']['name']);
    $uploadOk = 1;
    $FileType = pathinfo($target_file,PATHINFO_EXTENSION);

    if (file_exists($target_file)) 
    {
        $uploadOk = 2;
    }
    if ($_FILES["owl"]["size"] > 500000) 
    {
        echo "<script>alert('File Size too large.')</script>";
        $uploadOk = 0;
		header('Location:search.php?error=1');
    }

    if($FileType != "owls" ) 
    {
    echo "<script>alert('Sorry, only OWLS files are allowed.')</script>";
    $uploadOk = 0;
	header('Location:search.php?error=2');
    }
    if ($uploadOk == 0) 
    {
       header('Location: search.html');
    }
    else 
    {   
        move_uploaded_file($_FILES["owl"]["tmp_name"], $temp_file);
        $output = shell_exec('python Extract_up.py');
        if($output === false)
        {
            $output = shell_exec('rm temp_owl.owls');
            header('Location: search.html');
        }    
        $token = strtok($output, ":");
        $i=0;
        while ($token !== false)
        {
            $arr[ $i++ ] = $token;
            $token = strtok(":");
        }

        if($i === 2)
        {
            $_SESSION["inp"] = $arr[0];
            $_SESSION["out"] = $arr[1];
        }
        else
        {
            $_SESSION["inp"] = "";
            $_SESSION["out"] = "";
        }
         
        $_SESSION["theta"] = 0.5;
         
        if($uploadOk === 1)
        {
            echo $target_file;
            $output = shell_exec('cp temp_owl.owls '.$target_file);
        }
        $output = shell_exec('rm temp_owl.owls');
        header('Location: services.php');
    }
}
?>
