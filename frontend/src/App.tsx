import { Route, Routes } from "react-router-dom";
import { AppShell } from "@/components/AppShell";
import OverviewPage from "@/pages/OverviewPage";
import DocPage from "@/pages/DocPage";
import MatrixPage from "@/pages/MatrixPage";
import GapsPage from "@/pages/GapsPage";
import SearchPage from "@/pages/SearchPage";
import ArchitecturePage from "@/pages/ArchitecturePage";

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<OverviewPage />} />
        <Route path="/doc" element={<DocPage />} />
        <Route path="/matrix" element={<MatrixPage />} />
        <Route path="/gaps" element={<GapsPage />} />
        <Route path="/architecture" element={<ArchitecturePage />} />
        <Route path="/search" element={<SearchPage />} />
      </Routes>
    </AppShell>
  );
}
