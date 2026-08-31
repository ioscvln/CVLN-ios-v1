import { Route, Routes } from "react-router-dom";
import { AppShell } from "@/components/AppShell";
import OverviewPage from "@/pages/OverviewPage";
import DocPage from "@/pages/DocPage";
import MatrixPage from "@/pages/MatrixPage";
import GapsPage from "@/pages/GapsPage";
import SearchPage from "@/pages/SearchPage";
import ArchitecturePage from "@/pages/ArchitecturePage";
import FreezePage from "@/pages/FreezePage";
import DecisionsPage from "@/pages/DecisionsPage";
import RegistryPage from "@/pages/RegistryPage";
import GraphPage from "@/pages/GraphPage";
import KiltikonetPage from "@/pages/KiltikonetPage";

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<OverviewPage />} />
        <Route path="/doc" element={<DocPage />} />
        <Route path="/matrix" element={<MatrixPage />} />
        <Route path="/gaps" element={<GapsPage />} />
        <Route path="/architecture" element={<ArchitecturePage />} />
        <Route path="/freeze" element={<FreezePage />} />
        <Route path="/decisions" element={<DecisionsPage />} />
        <Route path="/registry" element={<RegistryPage />} />
        <Route path="/registry/:key" element={<RegistryPage />} />
        <Route path="/graph" element={<GraphPage />} />
        <Route path="/kiltikonet" element={<KiltikonetPage />} />
        <Route path="/search" element={<SearchPage />} />
      </Routes>
    </AppShell>
  );
}
