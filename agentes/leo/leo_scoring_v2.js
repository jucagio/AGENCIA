const fs = require('fs');

const leads = JSON.parse(fs.readFileSync('./leads_lote1_initial.json', 'utf8'));
console.log(`AJUSTANDO SCORING FRAMEWORK - LEO v2\n`);

const results = [];

for (const lead of leads) {
  const empleados = (lead.empleados_estimado || "").toLowerCase();
  let fit_size = 0;
  if (empleados.includes("40-100") || empleados.includes("35-80")) fit_size = 12;
  else if (empleados.includes("25-60") || empleados.includes("30-70")) fit_size = 11;
  else if (empleados.includes("20-50")) fit_size = 10;
  else fit_size = 6;

  const presupuesto = (lead.presupuesto_potencial || "$0").replace(/[$,/mes]/g, "").trim();
  let fit_budget = 5;
  try {
    const minBudget = parseInt(presupuesto.split("-")[0].trim());
    if (minBudget >= 2000) fit_budget = 15;
    else if (minBudget >= 1500) fit_budget = 13;
    else if (minBudget >= 1000) fit_budget = 11;
    else if (minBudget >= 800) fit_budget = 8;
  } catch (e) {}

  const dolores = (lead.dolores_identificados || []).length;
  const fit_dolor = Math.min(13, dolores * 4);
  const fit_score = Math.min(100, ((fit_size + fit_budget + fit_dolor) / 40) * 100);

  let urgencia_base = 50;
  if (lead.urgencia === "Hot") urgencia_base = 85;
  else if (lead.urgencia === "Warm") urgencia_base = 65;
  const urgencia_score = Math.min(100, urgencia_base);

  const review_count = parseInt(lead.review_count || 0);
  let momentum = 0;
  if (review_count > 5000) momentum = 100;
  else if (review_count > 4000) momentum = 90;
  else if (review_count > 3000) momentum = 75;
  else if (review_count > 2000) momentum = 60;
  else if (review_count > 1500) momentum = 50;
  else momentum = 30;

  let accesibilidad = 0;
  if (lead.contacto_email && lead.contacto_email.includes("@") && lead.contacto_email !== "N/A") accesibilidad += 5;
  if (lead.phone && lead.phone !== "N/A") accesibilidad += 5;
  if (lead.sitio_web && lead.sitio_web !== "N/A") accesibilidad += 5;

  let probabilidad = 0;
  if (lead.validacion === true) probabilidad += 3;
  if (lead.contacto_ideal_rol && lead.contacto_ideal_rol !== "N/A") probabilidad += 2;

  const score_final = (fit_score * 0.40) + (urgencia_score * 0.25) + (momentum * 0.15) + (accesibilidad * 0.15) + (probabilidad * 0.05);

  let prioridad = 4;
  if (score_final >= 85) prioridad = 1;
  else if (score_final >= 75) prioridad = 2;
  else if (score_final >= 65) prioridad = 3;

  let estrategia_contacto = "Llamada directa";
  if (lead.phone && lead.contacto_email && lead.contacto_email.includes("@")) {
    estrategia_contacto = "Email + WhatsApp + Llamada";
  } else if (lead.contacto_email && lead.contacto_email.includes("@")) {
    estrategia_contacto = "Email + WhatsApp";
  }

  const dolores_list = (lead.dolores_identificados || ["procesos manuales"])[0];
  const pitch = `Automatizar ${dolores_list.substring(0, 35)}. n8n/Make - Ahorra 4-6h/semana.`;

  results.push({
    id: lead.id,
    empresa: lead.empresa,
    pais: lead.pais,
    sector: lead.sector,
    score_fit: parseFloat(fit_score.toFixed(1)),
    score_urgencia: parseFloat(urgencia_score.toFixed(1)),
    score_momentum: parseFloat(momentum.toFixed(1)),
    score_accesibilidad: parseFloat(accesibilidad.toFixed(1)),
    score_probabilidad: parseFloat(probabilidad.toFixed(1)),
    score_final: parseFloat(score_final.toFixed(1)),
    prioridad,
    contacto_ideal: lead.contacto_ideal_rol,
    estrategia_contacto,
    pitch_corto: pitch,
    tiempo_venta_estimado: lead.urgencia === "Hot" ? "2-3 semanas" : "3-4 semanas",
    rating: lead.rating,
    review_count: lead.review_count,
    presupuesto_potencial: lead.presupuesto_potencial,
    email: lead.contacto_email,
    phone: lead.phone
  });
}

results.sort((a, b) => b.score_final - a.score_final);

const headers = ["id", "empresa", "pais", "sector", "score_fit", "score_urgencia", "score_momentum", "score_accesibilidad", "score_probabilidad", "score_final", "prioridad", "contacto_ideal", "estrategia_contacto", "pitch_corto", "tiempo_venta_estimado", "rating", "review_count", "presupuesto_potencial", "email", "phone"];

const csvContent = [
  headers.join(","),
  ...results.map(r => {
    const esc = (v) => {
      if (!v) return '""';
      return `"${String(v).replace(/"/g, '""')}"`;
    };
    return `${r.id},${esc(r.empresa)},${esc(r.pais)},${esc(r.sector)},${r.score_fit},${r.score_urgencia},${r.score_momentum},${r.score_accesibilidad},${r.score_probabilidad},${r.score_final},${r.prioridad},${esc(r.contacto_ideal)},${esc(r.estrategia_contacto)},${esc(r.pitch_corto)},${esc(r.tiempo_venta_estimado)},${r.rating},${r.review_count},${esc(r.presupuesto_potencial)},${esc(r.email)},${esc(r.phone)}`;
  })
].join("\n");

fs.writeFileSync('./leo_scoring_lote1.csv', csvContent, 'utf8');

console.log(`✓ Scoring v2 completed!\n`);

console.log(`=== TOP LEADS BY PRIORITY ===`);
console.log(`\nPRIORITY 1 (Score 85+) - APPROACH IMMEDIATELY:`);
const p1 = results.filter(r => r.prioridad === 1);
if (p1.length === 0) console.log(`  (No leads with 85+ score yet - model recalibrating)`);
p1.slice(0, 5).forEach((r, i) => {
  console.log(`  ${i+1}. ${r.empresa.substring(0, 28).padEnd(28)} | ${r.score_final} | $${r.presupuesto_potencial}`);
});

console.log(`\nPRIORITY 2 (Score 75-84) - WARM PROSPECTS:`);
const p2 = results.filter(r => r.prioridad === 2);
console.log(`  Found ${p2.length} leads`);
p2.slice(0, 8).forEach((r, i) => {
  console.log(`  ${i+1}. ${r.empresa.substring(0, 28).padEnd(28)} | ${r.score_final} | P${r.prioridad}`);
});

console.log(`\nPRIORITY 3 (Score 65-74) - BUILD RELATIONSHIP:`);
const p3 = results.filter(r => r.prioridad === 3);
console.log(`  Found ${p3.length} leads\n`);

console.log(`=== VALIDATION METRICS ===`);
const score_85 = results.filter(r => r.score_final >= 85).length;
const score_75 = results.filter(r => r.score_final >= 75).length;
const score_65 = results.filter(r => r.score_final >= 65).length;

console.log(`Leads P1 (85+): ${score_85}`);
console.log(`Leads P2 (75+): ${score_75}`);
console.log(`Leads P3 (65+): ${score_65}`);
console.log(`Total leads: ${results.length}`);

console.log(`\n=== LEO FRAMEWORK V2 ===`);
console.log(`Fit (40%): Tamaño + Presupuesto + Dolores`);
console.log(`Urgencia (25%): Lead status (Hot/Warm)`);
console.log(`Momentum (15%): Review count = tráfico/crecimiento`);
console.log(`Accesibilidad (15%): Email + Phone + Web`);
console.log(`Probabilidad (5%): Validación Yang + Contacto ideal`);

fs.writeFileSync('./leo_scoring_report.json', JSON.stringify(results, null, 2), 'utf8');
console.log(`\n✓ Full report saved: leo_scoring_report.json`);
