<?php
declare(strict_types=1);

namespace App\Domain\Portfolio\Repository;

interface PortfolioRepository
{
    public function list(): array;
    public function findById(int $id): ?array;
    public function create(array $data): int;
}
