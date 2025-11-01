export const formatNumber = (value) => {
  if (!value && value !== 0) return '0'
  return new Intl.NumberFormat('pt-BR').format(value)
}

export const formatCurrency = (value) => {
  if (!value && value !== 0) return 'R$ 0,00'
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

export const formatPercentage = (value) => {
  if (!value && value !== 0) return '0%'
  return new Intl.NumberFormat('pt-BR', {
    style: 'percent',
    minimumFractionDigits: 1,
    maximumFractionDigits: 2
  }).format(value / 100)
}