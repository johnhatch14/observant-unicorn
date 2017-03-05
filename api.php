<?php

$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : 'none';
$dat = isset($_GET['dat']) ? $_GET['dat'] : 'none';
$tok = isset($_GET['tok']) ? $_GET['tok'] : 'none';

$vtok = sha1('SUPER_SECRET_STRING' . $dat);

#if ($vtok != $tok) {die('INVALID AUTH');}

switch ($cmd) {
	case 'dmp' :
		$devices = json_decode(base64_decode($dat), true);
		if ($devices == NULL) {die("Failed to parse JSON string");}
		echo(var_dump($devices));
		if (($db = db_connect())->connect_errno) {
			die("Failed to connect to MySQL: (" . $db->connect_errno . ") " . $db->connect_error);
		}
		$i=0;
		foreach($devices as $dev_mac => $device) {
			$dev_lastSeen = $device['time'];
			$dev_assoc = $device['associated'];
			$dev_sensID = $device['sensor_id'];
			$dev_isAP = $device['ap'];
			$qres = $db->query("INSERT INTO `device`(`mac`, `lastSeen`, `associatedWith`, `isAP`) VALUES ('$dev_mac','$dev_lastSeen','$dev_assoc','$dev_isAP')");
			print(var_dump($db->error));
			print(var_dump($qres));
		}
		$res = $res->fetch_assoc();
		echo(var_dump($res));
		break;
}

function db_connect() {
	return new mysqli('localhost','unicorn','observant','unicorndb');
}

echo("Hello World!");

?>
