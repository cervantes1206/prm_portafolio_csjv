<?php
declare(strict_types=1);

namespace App\Infrastructure\Storage;

use App\Ports\Storage\FileStoragePort;

final class LocalFileStorage implements FileStoragePort
{
    public function __construct(private string $basePath) {}

    public function ensureDirs(array $relativeDirs): void
    {
        foreach ($relativeDirs as $dir) {
            $path = rtrim($this->basePath, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . trim($dir, '/\\');
            if (!is_dir($path)) mkdir($path, 0777, true);
        }
    }

    public function put(string $relativePath, string $content): string
    {
        $full = rtrim($this->basePath, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . trim($relativePath, '/\\');
        $dir = dirname($full);
        if (!is_dir($dir)) mkdir($dir, 0777, true);
        file_put_contents($full, $content);
        return $full;
    }
}
