import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import App from "./App";

const payload = {
  metrics: {
    selective_accuracy: 0.914, coverage: 0.789, review_rate: 0.211, ece_after: 0.0087,
    ece_before: 0.0255, threshold: 0.504, target_selective_accuracy: 0.9, test_count: 4050,
    sample_count: 27000, accuracy: 0.894, macro_f1: 0.889, per_class: { Forest: {} },
    inference_latency_ms: { median: 16.2, p95: 22.3, sample_count: 100 }, limitations: ["Scene classification only."],
  },
  demos: [{ file: "Forest_1.jpg", display_label: "Forest", story: "Clear forest", image_url: "/demo-assets/Forest_1.jpg" }],
  robustness: [], risk_coverage: [{ threshold: "0.3", selective_accuracy: "0.89" }, { threshold: "0.99", selective_accuracy: "0.998" }],
};

describe("TerraTrust interface", () => {
  it("loads evidence and navigates by accessible buttons", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => payload }));
    render(<App />);
    expect(await screen.findByRole("heading", { name: /see and understand the land clearly. act with stronger evidence/i })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /^analyze$/i }));
    await waitFor(() => expect(screen.getByRole("heading", { name: /land-cover analysis/i })).toBeInTheDocument());
    expect(screen.getByRole("button", { name: /run analysis/i })).toBeEnabled();
    fireEvent.click(screen.getByRole("button", { name: "Validation" }));
    expect(screen.getByRole("heading", { name: /targets, evidence, and method/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /sdg contribution/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /deployment path/i })).toBeInTheDocument();
  });
});
