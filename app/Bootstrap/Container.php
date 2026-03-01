<?php
declare(strict_types=1);

namespace App\Bootstrap;

use App\Infrastructure\Config\config;
use App\Infrastructure\Persistence\MySQL\PDOConnection;
use App\Infrastructure\Persistence\MySQL\PortfolioMySQLRepository;
use App\Infrastructure\Storage\LocalFileStorage;
use App\Infrastructure\Pdf\PdfGeneratorMPDF;

use App\Ports\Http\Controllers\HomeController;
use App\Ports\Http\Controllers\PortfolioController;
use App\Ports\Http\Controllers\CertificateController;

final class Container
{
    private array $instances = [];

    public function get(string $id): object
    {
        if (isset($this->instances[$id])) return $this->instances[$id];

        if ($id === config::class) return $this->instances[$id] = new config();

        if ($id === PDOConnection::class) {
            $cfg = $this->get(config::class);
            return $this->instances[$id] = new PDOConnection($cfg);
        }

        if ($id === PortfolioMySQLRepository::class) {
            return $this->instances[$id] = new PortfolioMySQLRepository($this->get(PDOConnection::class));
        }

        if ($id === LocalFileStorage::class) {
            $cfg = $this->get(config::class);
            return $this->instances[$id] = new LocalFileStorage($cfg->storagePath());
        }

        if ($id === PdfGeneratorMPDF::class) {
            return $this->instances[$id] = new PdfGeneratorMPDF();
        }

        if ($id === HomeController::class) return $this->instances[$id] = new HomeController();

        if ($id === PortfolioController::class) {
            return $this->instances[$id] = new PortfolioController(
                $this->get(PortfolioMySQLRepository::class)
            );
        }

        if ($id === CertificateController::class) {
            return $this->instances[$id] = new CertificateController(
                $this->get(PortfolioMySQLRepository::class),
                $this->get(PdfGeneratorMPDF::class),
                $this->get(LocalFileStorage::class)
            );
        }

        return $this->instances[$id] = new $id();
    }
}
