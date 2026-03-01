<?php
declare(strict_types=1);

namespace App\Infrastructure\Persistence\MySQL;

use PDO;
use App\Infrastructure\Config\config;

final class PDOConnection
{
    private PDO $pdo;

    public function __construct(config $cfg)
    {
        $dsn = "mysql:host={$cfg->dbHost()};dbname={$cfg->dbName()};charset=utf8mb4";
        $this->pdo = new PDO($dsn, $cfg->dbUser(), $cfg->dbPass(), [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        ]);
    }

    public function pdo(): PDO { return $this->pdo; }
}
