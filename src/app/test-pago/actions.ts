
"use server";

import { generateSongLyricsAndAudio, GenerateSongLyricsAndAudioInput } from "@/ai/flows/generate-song-lyrics-and-audio";
import { generateAlbumArt, GenerateAlbumArtInput } from "@/ai/flows/generate-album-art";
import { incorporateUserRequestsIntoSong, IncorporateUserRequestsIntoSongInput } from "@/ai/flows/incorporate-user-requests-into-song";
import { songCreationSchema, SongCreationFormValues } from "@/config/schemas";

import { z } from "zod";

export async function createSongAction(data: SongCreationFormValues) {
  try {
    const validatedData = songCreationSchema.parse(data);

    const flowInput: GenerateSongLyricsAndAudioInput = {
      email: validatedData.email,
      songType: validatedData.songType,
      dedicatedTo: validatedData.dedicatedTo,
      requester: validatedData.requester,
      nickname: validatedData.nickname,
      relationship: validatedData.relationship,
      story: validatedData.story,
      genre: validatedData.genre,
      genre2: validatedData.genre2,
      voice: validatedData.voice,
      includeNames: validatedData.includeNames,
      keywords: validatedData.keywords,
      referenceSong: validatedData.referenceSong,
      styleVoice: validatedData.styleVoice,
      instrumentation: validatedData.instrumentation,
      mood: validatedData.mood,
      tempo: validatedData.tempo,
      structure: validatedData.structure,
      ending: validatedData.ending,
      inspirationalArtist: validatedData.inspirationalArtist,
    };

    const result = await generateSongLyricsAndAudio(flowInput);

    if (!result.lyrics || !result.audio) {
      throw new Error("AI generation failed to produce lyrics or audio.");
    }

    return {
      lyrics: result.lyrics,
      audio: result.audio,
      error: null,
    };
  } catch (error) {
    console.error("[SONG_CREATION_ACTION_ERROR]", error);
    if (error instanceof z.ZodError) {
      return { lyrics: null, audio: null, error: "Invalid data provided.", details: error.issues };
    }
    const errorMessage = error instanceof Error ? error.message : "Failed to generate song. Please try again later.";
    return { lyrics: null, audio: null, error: errorMessage };
  }
}

const albumArtSchema = z.object({
  prompt: z.string().min(1, "Prompt for album art is required."),
});

export async function createAlbumArtAction(data: z.infer<typeof albumArtSchema>) {
    try {
        const validatedData = albumArtSchema.parse(data);
        const flowInput: GenerateAlbumArtInput = { prompt: validatedData.prompt };
        const result = await generateAlbumArt(flowInput);
        
        if (!result.imageUrl) {
            throw new Error("AI failed to generate album art.");
        }
        
        return { imageUrl: result.imageUrl, error: null };
    } catch (error) {
        console.error("[ALBUM_ART_ACTION_ERROR]", error);
        const errorMessage = error instanceof Error ? error.message : "Failed to generate album art.";
        return { imageUrl: null, error: errorMessage };
    }
}


const revisionSchema = z.object({
    lyricsDraft: z.string(),
    requests: z.string(),
    songDetails: songCreationSchema,
});


export async function reviseSongAction(data: z.infer<typeof revisionSchema>) {
    try {
        const validatedData = revisionSchema.parse(data);
        
        const flowInput: IncorporateUserRequestsIntoSongInput = {
            lyricsDraft: validatedData.lyricsDraft,
            requests: validatedData.requests,
            songDetails: validatedData.songDetails,
        };
        
        const result = await incorporateUserRequestsIntoSong(flowInput);

        if (!result.revisedLyrics || !result.revisedAudio) {
            throw new Error("AI failed to revise song.");
        }
        
        return {
            lyrics: result.revisedLyrics,
            audio: result.revisedAudio,
            error: null,
        };

    } catch (error) {
        console.error("[REVISE_SONG_ACTION_ERROR]", error);
        const errorMessage = error instanceof Error ? error.message : "Failed to revise song.";
        return { lyrics: null, audio: null, error: errorMessage };
    }
}
