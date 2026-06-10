import AskBox from "@/components/AskBox";
import TableBrowser from "@/components/TableBrowser";

export default function Home() {
  return (
    <main>
      <header className="app-header">
        <h1>text2sql — pregled baze i pitanja</h1>
      </header>
      <div className="wrap">
        <AskBox />
        <TableBrowser />
      </div>
    </main>
  );
}
