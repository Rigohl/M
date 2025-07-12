
'use server';
/**
 * @fileOverview A Genkit flow to incorporate user requests into a generated song and regenerate the audio.
 *
 * - incorporateUserRequestsIntoSong - A function that handles the incorporation of user requests into a song.
 * - IncorporateUserRequestsIntoSongInput - The input type for the incorporateUserRequestsIntoSong function.
 * - IncorporateUserRequestsIntoSongOutput - The return type for the incorporateUserRequestsIntoSong function.
 */

import {ai} from '@/ai/genkit';
import {googleAI} from '@genkit-ai/googleai';
import {toWav} from '@/lib/audio';
import { z } from 'zod';
import { songCreationSchema, SongCreationFormValues } from '@/config/schemas';

const IncorporateUserRequestsIntoSongInputSchema = z.object({
  lyricsDraft: z.string().describe('The initial draft of the song lyrics.'),
  requests: z.string().describe('Specific requests from the user for changing the song.'),
  songDetails: songCreationSchema.describe("The original parameters of the song for context."),
});
export type IncorporateUserRequestsIntoSongInput = z.infer<typeof IncorporateUserRequestsIntoSongInputSchema>;

const IncorporateUserRequestsIntoSongOutputSchema = z.object({
  revisedLyrics: z.string().describe('The revised song lyrics incorporating user requests.'),
  revisedAudio: z.string().describe('The re-generated audio for the revised song as a base64 encoded data URI.'),
});
export type IncorporateUserRequestsIntoSongOutput = z.infer<typeof IncorporateUserRequestsIntoSongOutputSchema>;

export async function incorporateUserRequestsIntoSong(input: IncorporateUserRequestsIntoSongInput): Promise<IncorporateUserRequestsIntoSongOutput> {
  return incorporateUserRequestsIntoSongFlow(input);
}

const revisionPrompt = ai.definePrompt({
  name: 'reviseLyricsPrompt',
  input: {schema: IncorporateUserRequestsIntoSongInputSchema},
  output: {schema: z.object({ revisedLyrics: z.string() })},
  config: {
    safetySettings: [
      {
        category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
        threshold: 'BLOCK_ONLY_HIGH',
      },
      {
        category: 'HARM_CATEGORY_HATE_SPEECH',
        threshold: 'BLOCK_MEDIUM_AND_ABOVE',
      },
       {
        category: 'HARM_CATEGORY_HARASSMENT',
        threshold: 'BLOCK_MEDIUM_AND_ABOVE',
      },
    ],
  },
<<<<<<< HEAD
  prompt: `You are a professional songwriter revising a song based on client feedback.
Your goal is to intelligently incorporate the requested changes into the existing lyrics. Maintain the song's original tone, style, and core story as much as possible unless the request specifically asks to change it.

Here is the original song context:
- Song Type: {{songDetails.songType}}
- Genre: {{songDetails.genre}}
- Dedicated to: {{songDetails.dedicatedTo}} from {{songDetails.requester}}
- Story: {{{songDetails.story}}}
{{#if songDetails.inspirationalArtist}}
- Inspirational Style: {{{songDetails.inspirationalArtist}}}
{{/if}}
- Estilo vocal del borrador original (si aplica): {{#if songDetails.styleVoice}}Inspirado en {{songDetails.styleVoice}}{{else}}Voz estándar{{/if}}

Here is the current draft of the lyrics:
--- LYRICS DRAFT ---
=======
  prompt: `Eres un compositor profesional revisando una canción basándote en los comentarios de un cliente.
Tu objetivo es incorporar de manera inteligente los cambios solicitados en la letra existente. Mantén el tono, el estilo y la historia central originales de la canción.

Contexto original de la canción:
- Género: {{songDetails.genre}}
- Historia: {{{songDetails.story}}}

Borrador actual de la letra:
--- BORRADOR DE LETRA ---
>>>>>>> ff6d6df (ya puedo crear canciones?)
{{{lyricsDraft}}}
--- FIN DEL BORRADOR ---

<<<<<<< HEAD
Here are the client's revision requests:
--- CLIENT REQUESTS ---
=======
Solicitudes de revisión del cliente:
--- SOLICITUDES DEL CLIENTE ---
>>>>>>> ff6d6df (ya puedo crear canciones?)
{{{requests}}}
--- FIN DE SOLICITUDES ---

Por favor, genera la nueva letra revisada para la canción. Solo la letra.
`,
});


const incorporateUserRequestsIntoSongFlow = ai.defineFlow(
  {
    name: 'incorporateUserRequestsIntoSongFlow',
    inputSchema: IncorporateUserRequestsIntoSongInputSchema,
    outputSchema: IncorporateUserRequestsIntoSongOutputSchema,
  },
  async (input) => {
    // 1. Generate revised lyrics
    const revisionResponse = await revisionPrompt(input);
    const revisedLyrics = revisionResponse.output?.revisedLyrics;

    if (!revisedLyrics) {
      throw new Error('Failed to generate revised lyrics.');
    }

    // 2. Generate new audio from the revised lyrics
    const voiceMap: { [key: string]: string } = {
      'male-deep': 'rasalgethi',
      'male-standard': 'algenib',
      'male-youthful': 'puck',
      'female-soft': 'laomedeia',
      'female-standard': 'achernar',
      'female-energetic': 'schedar',
    };
    const voiceName = voiceMap[input.songDetails.voice] || 'algenib';

    const { media } = await ai.generate({
      model: googleAI.model('gemini-2.5-flash-preview-tts'),
      config: {
        responseModalities: ['AUDIO'],
        speechConfig: {
          voiceConfig: {
            prebuiltVoiceConfig: { voiceName },
          },
        },
      },
      prompt: revisedLyrics,
    });

    if (!media) {
      throw new Error('Failed to generate audio for revised lyrics.');
    }
    
    const audioBuffer = Buffer.from(
      media.url.substring(media.url.indexOf(',') + 1),
      'base64'
    );
    const audioWavBase64 = await toWav(audioBuffer);

    return {
      revisedLyrics,
      revisedAudio: 'data:audio/wav;base64,' + audioWavBase64,
    };
  }
);
