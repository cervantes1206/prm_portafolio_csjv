<?php
declare(strict_types=1);

namespace App\Ports\Http\Controllers;

use App\Domain\Portfolio\Repository\PortfolioRepository;

final class PortfolioController
{
    public function __construct(private PortfolioRepository $repo) {}

    public function list(): void
    {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($this->repo->list());
    }

    public function show(): void
    {
        $id = (int)($_GET['id'] ?? 0);
        $row = $id ? $this->repo->findById($id) : null;

        if (!$row) { http_response_code(404); echo "Portfolio no encontrado"; return; }

        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($row);
    }

    public function create(): void
    {
        $data = $_POST ?: json_decode((string)file_get_contents('php://input'), true) ?: [];
        $id = $this->repo->create($data);

        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['created_id' => $id]);
    }
}
