<?php
declare(strict_types=1);

namespace App\Infrastructure\Config;

use Dotenv\Dotenv;

final class config
{
    public function __construct()
    {
        $root = dirname(__DIR__, 3);
        if (file_exists($root . '/.env')) {
            $dotenv = Dotenv::createImmutable($root);
            $dotenv->safeLoad();
        }
    }

    public function dbHost(): string { return $_ENV['DB_HOST'] ?? '127.0.0.1'; }
    public function dbName(): string { return $_ENV['DB_NAME'] ?? 'prm_portafolio'; }
    public function dbUser(): string { return $_ENV['DB_USER'] ?? 'root'; }
    public function dbPass(): string { return $_ENV['DB_PASS'] ?? ''; }

    public function storagePath(): string
    {
        $root = dirname(__DIR__, 3);
        return $_ENV['STORAGE_PATH'] ?? ($root . '/storage');
    }
}
