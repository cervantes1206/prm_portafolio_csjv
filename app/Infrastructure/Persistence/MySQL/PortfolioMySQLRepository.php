<?php
declare(strict_types=1);

namespace App\Infrastructure\Persistence\MySQL;

use App\Domain\Portfolio\Repository\PortfolioRepository;
use PDO;

final class PortfolioMySQLRepository implements PortfolioRepository
{
    public function __construct(private PDOConnection $conn) {}

    public function list(): array
    {
        $stmt = $this->conn->pdo()->query("SELECT id, nombre, grado, created_at FROM estudiantes ORDER BY id DESC");
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    public function findById(int $id): ?array
    {
        $stmt = $this->conn->pdo()->prepare("SELECT * FROM estudiantes WHERE id = :id");
        $stmt->execute(['id' => $id]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        return $row ?: null;
    }

    public function create(array $data): int
    {
        $sql = "INSERT INTO estudiantes
            (nombre, grado, frase_personal, fortalezas, retos, talentos, intereses, experiencias, logros, estudios, valores, trayectoria)
            VALUES
            (:nombre, :grado, :frase, :fortalezas, :retos, :talentos, :intereses, :experiencias, :logros, :estudios, :valores, :trayectoria)";
        $stmt = $this->conn->pdo()->prepare($sql);
        $stmt->execute([
            'nombre' => $data['nombre'] ?? '',
            'grado' => $data['grado'] ?? '',
            'frase' => $data['frase_personal'] ?? '',
            'fortalezas' => $data['fortalezas'] ?? '',
            'retos' => $data['retos'] ?? '',
            'talentos' => $data['talentos'] ?? '',
            'intereses' => $data['intereses'] ?? '',
            'experiencias' => $data['experiencias'] ?? '',
            'logros' => $data['logros'] ?? '',
            'estudios' => $data['estudios'] ?? '',
            'valores' => $data['valores'] ?? '',
            'trayectoria' => $data['trayectoria'] ?? '',
        ]);
        return (int)$this->conn->pdo()->lastInsertId();
    }
}
