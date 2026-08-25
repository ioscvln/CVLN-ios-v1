import type { ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useNavigate } from "react-router-dom";
import { Mermaid } from "./Mermaid";
import { slugify } from "@/lib/slug";

/** Resolve a relative Markdown link against the current document's directory. */
function resolveCorpusPath(href: string, currentPath: string): string | null {
  if (/^[a-z]+:/i.test(href) || href.startsWith("#")) return null;
  const [rawPath, hash] = href.split("#");
  if (!rawPath.endsWith(".md")) return null;
  const dir = currentPath.split("/").slice(0, -1);
  const parts = rawPath.split("/");
  const stack = [...dir];
  for (const part of parts) {
    if (part === "." || part === "") continue;
    if (part === "..") stack.pop();
    else stack.push(part);
  }
  return stack.join("/") + (hash ? `#${hash}` : "");
}

function textOf(node: ReactNode): string {
  if (typeof node === "string" || typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(textOf).join("");
  if (node && typeof node === "object" && "props" in node) {
    return textOf((node as { props: { children?: ReactNode } }).props.children);
  }
  return "";
}

export function Markdown({ content, docPath }: { content: string; docPath: string }) {
  const navigate = useNavigate();

  return (
    <div className="cvln-prose" data-testid="markdown-body">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => <h1 id={slugify(textOf(children))}>{children}</h1>,
          h2: ({ children }) => <h2 id={slugify(textOf(children))}>{children}</h2>,
          h3: ({ children }) => <h3 id={slugify(textOf(children))}>{children}</h3>,
          table: ({ children }) => (
            <div className="cvln-table-wrap">
              <table>{children}</table>
            </div>
          ),
          a: ({ href, children }) => {
            const target = href ? resolveCorpusPath(href, docPath) : null;
            if (target) {
              return (
                <a
                  href={`/doc?path=${encodeURIComponent(target.split("#")[0])}`}
                  data-testid="doc-internal-link"
                  onClick={(e) => {
                    e.preventDefault();
                    navigate(`/doc?path=${encodeURIComponent(target.split("#")[0])}`);
                  }}
                >
                  {children}
                </a>
              );
            }
            return (
              <a href={href} target="_blank" rel="noreferrer" data-testid="doc-external-link">
                {children}
              </a>
            );
          },
          code: ({ className, children, ...rest }) => {
            const lang = /language-(\w+)/.exec(className ?? "")?.[1];
            const raw = String(children ?? "").replace(/\n$/, "");
            if (lang === "mermaid") return <Mermaid code={raw} />;
            if (lang) {
              return (
                <span className="relative block">
                  <span className="pointer-events-none absolute right-2 top-2 font-mono text-[10px] uppercase tracking-[0.14em] text-slate-500">
                    {lang}
                  </span>
                  <code className={className} {...rest}>
                    {children}
                  </code>
                </span>
              );
            }
            return (
              <code className={className} {...rest}>
                {children}
              </code>
            );
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
