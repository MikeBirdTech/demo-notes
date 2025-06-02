import ollama from 'ollama'

async function main() {
  const response = await ollama.chat({
    model: 'qwen3',
    messages: [
      {
        role: 'user',
        content: 'What is bigger, 9.9 or 9.11?',
      },
    ],
    stream: false,
    think: true,
  })

  console.log('Thinking:\n========\n\n' + response.message.thinking)
  console.log('\nResponse:\n========\n\n' + response.message.content + '\n\n')
}

main()