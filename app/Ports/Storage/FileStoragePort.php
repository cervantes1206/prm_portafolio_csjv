<?php
declare(strict_types=1);

namespace App\Ports\Storage;

interface FileStoragePort
{
    public function put(string $relativePath, string $content): string;
    public function ensureDirs(array $relativeDirs): void;
}
