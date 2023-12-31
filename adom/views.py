from django.shortcuts import render
from music21 import note, stream, tempo, configure, chord
import re
import music21
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect
from django.http import HttpResponse
# from .models import NoteList

def music_view2(request):
    clicked_value = request.session.get('clicked_value', None)
    print('Don')
    print(clicked_value)
    if request.method == 'POST':
        clik = request.POST.get('clicked_')
        score = music21.converter.parse("C:\\Users\\KOFI ADUKPO\\Desktop\\code\\aseda\\adom\\templates\\848.xml")
        # path = C:\Users\KOFI ADUKPO\Downloads\solfa\\{}
        # score = music21.converter.parse(path)
        # C:\Users\KOFI ADUKPO\Downloads\solfa
        # score = music21.converter.parse(path)


        # Initialize a list to store notes and rests at each point in time
        notes_and_rests_by_time = []
        notes_and_rests_by_time_ = []


        # Get all the notes, chords, and rests from the score
        all_notes = score.flat.getElementsByClass(music21.note.GeneralNote)

        # Create a dictionary to group elements by their starting offset
        elements_by_offset = {}

        # Iterate through the notes, chords, and rests and group them by offset
        for element in all_notes:
            offset = element.offset
            if offset not in elements_by_offset:
                elements_by_offset[offset] = []
            elements_by_offset[offset].append(element)

        # Sort the offsets in ascending order
        sorted_offsets = sorted(elements_by_offset.keys())

        notss = []

        # Iterate through the sorted offsets and collect notes and rests at each point in time
        for offset in sorted_offsets:
            elements = elements_by_offset[offset]
            notes_and_rests = []
            nots=[]

            for element in elements:
                if isinstance(element, music21.note.Note):
                    pitch = element.pitch
                    parts = re.split(r'(\d+)', str(pitch))
                    modified_item = ''.join(parts)
                    pitch = modified_item
                    notes_and_rests.append(f"{pitch}") # {element.duration.quarterLength}
                    nots.append(f"{pitch} {element.duration.quarterLength}")


                elif isinstance(element, music21.chord.Chord):
                    for chord_note in element:
                        chord_pitch = chord_note.pitch
                        parts = re.split(r'(\d+)', str(chord_pitch))
                        modified_item = ''.join(parts)
                        chord_pitch = modified_item
                        notes_and_rests.append(f"{chord_pitch}") # {chord_note.duration.quarterLength}
                        nots.append(f"{chord_pitch} {chord_note.duration.quarterLength}")

                elif isinstance(element, music21.note.Rest):
                    pass
                    # notes_and_rests.append(f"Rest Duration: {element.duration.quarterLength}")

            notes_and_rests_by_time.append(notes_and_rests)
            notes_and_rests_by_time_.append(nots)
            

        # # Print the notes and rests grouped by time
        # for i, notes_and_rests in enumerate(notes_and_rests_by_time):
        #     print(f"Time {i}: {', '.join(notes_and_rests)}")

        p = [['E-4 6.0'],['C4 1.0', 'E-4 6.0', 'A-2 1.0', 'A-3 3.0'], ['C4 1.0', 'C4 2.0', 'A-2 1.0', 'A-3 2.0'], ['E-4 1.0', 'C3 1.0']]
        p=notes_and_rests_by_time_
        t = []
        main = []
        data = p
        k=p

        ##taking care of the .75
        heavy=[]
        # Check if the decimal ends with .75
        for r in k:
            qw=[]
            qe=[]
            for u in r:
                pitch, duration = u.split()
                duration_float = float(duration)
                if duration_float % 1 == 0.75:
                    # Subtract 0.25 from it
                    new_duration = duration_float - 0.25
                    qw.append(f"{pitch} {new_duration:.1f}")
                    qe.append(f"{pitch} 0.25")
                else:
                    qw.append(u)
            heavy.append(qw)
            if qe:
                heavy.append(qe)

        k=heavy

        # Create a new list to store the modified elements
        # Create a new list to store the modified elements
        new_k = []

        # Iterate through the sublists in 'k'
        for sublist_k in k:
            modified_sublist = []
            remaining_sublist = []
            for element in sublist_k:
                pitch, duration = element.split()  # Split the element into pitch and duration
                duration_float = float(duration)  # Convert duration to a float
                if duration_float > 1.0:
                    if duration_float % 1 == 0.5:
                        # If duration ends with '.5', subtract 0.5 and add '.0' to the duration
                        modified_duration = f"{duration_float - 0.5:.1f}"
                        modified_sublist.append(f"{pitch} {modified_duration}")
                        remaining_sublist.append(f"{pitch} 0.5")  # Add a new element with '0.5' duration
                    else:
                        # If duration is odd and greater than 1.0, subtract 1.0 and create a sublist for it
                        modified_duration = f"{duration_float - 1.0:.1f}"
                        modified_sublist.append(f"{pitch} {modified_duration}")
                        remaining_sublist.append(f"{pitch} 1.0")
                else:
                    # Otherwise, keep the original element in the modified sublist
                    modified_sublist.append(element)
            new_k.append(modified_sublist)
            if remaining_sublist:
                new_k.append(remaining_sublist)
        p=new_k

        for i in p:


            if i:

                # Calculate the minimum duration in the list
                # print(i)
                min_duration = min(float(note.split()[1]) for note in i)

                # Create a new list with equal durations
                equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in i]
                t.append(equal_duration_list)

                # Create a remainder list with the original durations
                remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in i if float(note.split()[1]) > min_duration]
                if remainder:
                    # Extract the second items from each element
                    second_items = [float(note.split()[1]) for note in remainder]

                    # Check if all second items are the same
                    is_same_duration = all(item == second_items[0] for item in second_items)

                    if is_same_duration:
                        t.append(remainder)
                    else:
                        min_duration = min(float(note.split()[1]) for note in remainder) #leevel
                        # Create a new list with equal durations
                        equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
                        t.append(equal_duration_list)
                        # Create a remainder list with the original durations
                        remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in remainder if float(note.split()[1]) > min_duration]
                        # print(f'firstremain: {remainder}')
                        # Extract the second items from each element
                        if remainder:
                            second_items = [float(note.split()[1]) for note in remainder]
                            

                            # Check if all second items are the same
                            is_same_duration = all(item == second_items[0] for item in second_items)

                            if is_same_duration:
                                t.append(remainder)
                            else:
                                min_duration = min(float(note.split()[1]) for note in remainder)
                                # Create a new list with equal durations
                                equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
                                t.append(equal_duration_list)
                                ##
                                remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in remainder if float(note.split()[1]) > min_duration]
                                # Extract the second items from each element
                                # print(f'remain: {remainder}')
                                if remainder:
                                    second_items = [float(note.split()[1]) for note in remainder]

                                    # Check if all second items are the same
                                    is_same_duration = all(item == second_items[0] for item in second_items)

                                    if is_same_duration:
                                        # print(remainder)
                                        t.append(remainder)

                                    else:
                                        min_duration = min(float(note.split()[1]) for note in remainder)
                                        # Create a new list with equal durations
                                        equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
                                        t.append(equal_duration_list)
                                        remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in remainder if float(note.split()[1]) > min_duration]

                                        if remainder:
                                            second_items = [float(note.split()[1]) for note in remainder]

                                            # Check if all second items are the same
                                            is_same_duration = all(item == second_items[0] for item in second_items)

                                            if is_same_duration:
                                                t.append(remainder)
                                            else:
                                                min_duration = min(float(note.split()[1]) for note in remainder)
                                                # Create a new list with equal durations
                                                equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
                                                t.append(equal_duration_list)



            p = t
        new_p = []

        for f in p:
            pp=[]
            pl=[]
            for y in f:
                pitch, duration = y.split()
                duration_float = float(duration)

                if duration_float > 2.0 and duration_float % 2 == 1.0:
                    # If duration is greater than or equal to 1.0 and odd, subtract 1.0 from it
                    new_duration = duration_float - 1.0
                    pp.append(f"{pitch} {new_duration:.1f}")
                    pl.append(f"{pitch} 1.0")
                else:
                    pp.append(y)
            new_p.append(pp)
            if pl:
                new_p.append(pl)



        t=new_p

        data = t

        # Find the highest value of the second item in each sublist
        max_values = [max(float(note.split()[1]) for note in sublist) for sublist in data]

        # Modify 'data' to contain the highest values as sublists
        durate = [[max_value] for max_value in max_values]
        timer = durate.copy()


        data = t

        # Remove the second items in each element in the sublists
        modified_data = [[note.split()[0] for note in sublist] for sublist in data]


        # Define the mapping of durations to names
        duration_names = {0.5: 'eighth',1.0: 'quarter',0.25: '16th', 2.0: 'half', 4.0: 'whole'}

        # Given list 'p'
        p = durate

        # Convert 'p' to their names
        durate = [[duration_names[d] for d in sublist] for sublist in p]

        data = t

        # Remove the second items in each element in the sublists
        modified_data = [[note.split()[0] for note in sublist] for sublist in data]

        # Define the chords as lists of note names
        chords = modified_data
        chords = [[i, *sublist] for i, sublist in enumerate(chords)]
        # Define the durations for each chord
        durations = durate
        # Create a stream to store the notes
        music_stream = stream.Stream()
        # music_stream.append(tempo.MetronomeMark(number=500))
        # Iterate through the chords and durations
        for i, chord_notes in enumerate(chords):
            if i < len(durations):
                chord_obj = chord.Chord(chord_notes)
                chord_obj.duration.type = (durations[i])[0]
                music_stream.append(chord_obj)
            else:
                pass
                # print(f"Warning: Not enough durations provided for chord {i + 1}. Skipping.")
        # total_duration = music_stream.duration.quarterLength
        # music_stream.show('midi')
        ##
        in_midi = []
        

        try:
            # action = data.get('action')
            action = request.POST.get('action')

            if action == None:
                music_stream.show('midi')
            data = json.loads(request.body.decode('utf-8'))
            values = data.get('values')

            if len(values) == 2:
                

                # Extract the selected values and their colors
                value1 = values[0]['value']
                color1 = values[0]['color']
                value2 = values[1]['value']
                color2 = values[1]['color']
                print(value1)
                print(value2)
                if value1 > value2:
                    chords = chords[value2:value1]
                    durations = durations[value2:value1]   
                else:
                    chords = chords[value1:value2]
                    durations = durations[value1:value2]
                music_stream = stream.Stream()
                # music_stream.append(tempo.MetronomeMark(number=500))
                # Iterate through the chords and durations
                for i, chord_notes in enumerate(chords):
                    if i < len(durations):
                        chord_obj = chord.Chord(chord_notes)
                        chord_obj.duration.type = (durations[i])[0]
                        music_stream.append(chord_obj)
                    else:
                        pass
                        # print(f"Warning: Not enough durations provided for chord {i + 1}. Skipping.")
                # total_duration = music_stream.duration.quarterLength
                music_stream.show('midi')
                # Handle the selected objects based on their colors
                if color1 == 'highlight-yellow':
                    pass
                    # Handle the first selected object with a yellow highlight
                    # Your logic here...

                if color2 == 'highlight-green':
                    pass
                    # Handle the second selected object with a green highlight
                    # Your logic here...

            # For demonstration purposes, simply return the processed data
                # return JsonResponse({'message': 'Data received and processed successfully'})
                return render(request, 'home.html', {'timer':timer, 'chords':chords})
        except json.JSONDecodeError:
            # return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            return render(request, 'home.html', {'timer':timer, 'chords':chords})
        # return render(request, 'home.html', {'timer':timer, 'chords':chords})
    else:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        # return render(request, 'base.html', {})

    # if request.method == 'POST':
    #     solta = request.POST.get('clicked_')
    #     trim = request.POST.get('ssolta')
    #     print(f"solta {trim}")
    #     # score = music21.converter.parse("C:\\Users\\KOFI ADUKPO\\Desktop\\code\\aseda\\adom\\templates\\848.xml")
    #     path= f"C:\\Users\\KOFI ADUKPO\\Downloads\\solfa\\{solta}.xml"
    #     score = music21.converter.parse(path)
    #     # C:\Users\KOFI ADUKPO\Downloads\solfa
    #     score = music21.converter.parse(path) 


    #     # Initialize a list to store notes and rests at each point in time
    #     notes_and_rests_by_time = []
    #     notes_and_rests_by_time_ = []


    #     # Get all the notes, chords, and rests from the score
    #     all_notes = score.flat.getElementsByClass(music21.note.GeneralNote)

    #     # Create a dictionary to group elements by their starting offset
    #     elements_by_offset = {}

    #     # Iterate through the notes, chords, and rests and group them by offset
    #     for element in all_notes:
    #         offset = element.offset
    #         if offset not in elements_by_offset:
    #             elements_by_offset[offset] = []
    #         elements_by_offset[offset].append(element)

    #     # Sort the offsets in ascending order
    #     sorted_offsets = sorted(elements_by_offset.keys())

    #     notss = []

    #     # Iterate through the sorted offsets and collect notes and rests at each point in time
    #     for offset in sorted_offsets:
    #         elements = elements_by_offset[offset]
    #         notes_and_rests = []
    #         nots=[]

    #         for element in elements:
    #             if isinstance(element, music21.note.Note):
    #                 pitch = element.pitch
    #                 parts = re.split(r'(\d+)', str(pitch))
    #                 modified_item = ''.join(parts)
    #                 pitch = modified_item
    #                 notes_and_rests.append(f"{pitch}") # {element.duration.quarterLength}
    #                 nots.append(f"{pitch} {element.duration.quarterLength}")


    #             elif isinstance(element, music21.chord.Chord):
    #                 for chord_note in element:
    #                     chord_pitch = chord_note.pitch
    #                     parts = re.split(r'(\d+)', str(chord_pitch))
    #                     modified_item = ''.join(parts)
    #                     chord_pitch = modified_item
    #                     notes_and_rests.append(f"{chord_pitch}") # {chord_note.duration.quarterLength}
    #                     nots.append(f"{chord_pitch} {chord_note.duration.quarterLength}")

    #             elif isinstance(element, music21.note.Rest):
    #                 pass
    #                 # notes_and_rests.append(f"Rest Duration: {element.duration.quarterLength}")

    #         notes_and_rests_by_time.append(notes_and_rests)
    #         notes_and_rests_by_time_.append(nots)
            

    #     # # Print the notes and rests grouped by time
    #     # for i, notes_and_rests in enumerate(notes_and_rests_by_time):
    #     #     print(f"Time {i}: {', '.join(notes_and_rests)}")

    #     p = [['E-4 6.0'],['C4 1.0', 'E-4 6.0', 'A-2 1.0', 'A-3 3.0'], ['C4 1.0', 'C4 2.0', 'A-2 1.0', 'A-3 2.0'], ['E-4 1.0', 'C3 1.0']]
    #     p=notes_and_rests_by_time_
    #     t = []
    #     main = []
    #     data = p
    #     k=p

    #     ##taking care of the .75
    #     heavy=[]
    #     # Check if the decimal ends with .75
    #     for r in k:
    #         qw=[]
    #         qe=[]
    #         for u in r:
    #             pitch, duration = u.split()
    #             duration_float = float(duration)
    #             if duration_float % 1 == 0.75:
    #                 # Subtract 0.25 from it
    #                 new_duration = duration_float - 0.25
    #                 qw.append(f"{pitch} {new_duration:.1f}")
    #                 qe.append(f"{pitch} 0.25")
    #             else:
    #                 qw.append(u)
    #         heavy.append(qw)
    #         if qe:
    #             heavy.append(qe)

    #     k=heavy

    #     # Create a new list to store the modified elements
    #     # Create a new list to store the modified elements
    #     new_k = []

    #     # Iterate through the sublists in 'k'
    #     for sublist_k in k:
    #         modified_sublist = []
    #         remaining_sublist = []
    #         for element in sublist_k:
    #             pitch, duration = element.split()  # Split the element into pitch and duration
    #             duration_float = float(duration)  # Convert duration to a float
    #             if duration_float > 1.0:
    #                 if duration_float % 1 == 0.5:
    #                     # If duration ends with '.5', subtract 0.5 and add '.0' to the duration
    #                     modified_duration = f"{duration_float - 0.5:.1f}"
    #                     modified_sublist.append(f"{pitch} {modified_duration}")
    #                     remaining_sublist.append(f"{pitch} 0.5")  # Add a new element with '0.5' duration
    #                 else:
    #                     # If duration is odd and greater than 1.0, subtract 1.0 and create a sublist for it
    #                     modified_duration = f"{duration_float - 1.0:.1f}"
    #                     modified_sublist.append(f"{pitch} {modified_duration}")
    #                     remaining_sublist.append(f"{pitch} 1.0")
    #             else:
    #                 # Otherwise, keep the original element in the modified sublist
    #                 modified_sublist.append(element)
    #         new_k.append(modified_sublist)
    #         if remaining_sublist:
    #             new_k.append(remaining_sublist)
    #     p=new_k

    #     for i in p:


    #         if i:

    #             # Calculate the minimum duration in the list
    #             # print(i)
    #             min_duration = min(float(note.split()[1]) for note in i)

    #             # Create a new list with equal durations
    #             equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in i]
    #             t.append(equal_duration_list)

    #             # Create a remainder list with the original durations
    #             remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in i if float(note.split()[1]) > min_duration]
    #             if remainder:
    #                 # Extract the second items from each element
    #                 second_items = [float(note.split()[1]) for note in remainder]

    #                 # Check if all second items are the same
    #                 is_same_duration = all(item == second_items[0] for item in second_items)

    #                 if is_same_duration:
    #                     t.append(remainder)
    #                 else:
    #                     min_duration = min(float(note.split()[1]) for note in remainder) #leevel
    #                     # Create a new list with equal durations
    #                     equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
    #                     t.append(equal_duration_list)
    #                     # Create a remainder list with the original durations
    #                     remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in remainder if float(note.split()[1]) > min_duration]
    #                     # print(f'firstremain: {remainder}')
    #                     # Extract the second items from each element
    #                     if remainder:
    #                         second_items = [float(note.split()[1]) for note in remainder]
                            

    #                         # Check if all second items are the same
    #                         is_same_duration = all(item == second_items[0] for item in second_items)

    #                         if is_same_duration:
    #                             t.append(remainder)
    #                         else:
    #                             min_duration = min(float(note.split()[1]) for note in remainder)
    #                             # Create a new list with equal durations
    #                             equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
    #                             t.append(equal_duration_list)
    #                             ##
    #                             remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in remainder if float(note.split()[1]) > min_duration]
    #                             # Extract the second items from each element
    #                             # print(f'remain: {remainder}')
    #                             if remainder:
    #                                 second_items = [float(note.split()[1]) for note in remainder]

    #                                 # Check if all second items are the same
    #                                 is_same_duration = all(item == second_items[0] for item in second_items)

    #                                 if is_same_duration:
    #                                     # print(remainder)
    #                                     t.append(remainder)

    #                                 else:
    #                                     min_duration = min(float(note.split()[1]) for note in remainder)
    #                                     # Create a new list with equal durations
    #                                     equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
    #                                     t.append(equal_duration_list)
    #                                     remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in remainder if float(note.split()[1]) > min_duration]

    #                                     if remainder:
    #                                         second_items = [float(note.split()[1]) for note in remainder]

    #                                         # Check if all second items are the same
    #                                         is_same_duration = all(item == second_items[0] for item in second_items)

    #                                         if is_same_duration:
    #                                             t.append(remainder)
    #                                         else:
    #                                             min_duration = min(float(note.split()[1]) for note in remainder)
    #                                             # Create a new list with equal durations
    #                                             equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
    #                                             t.append(equal_duration_list)



    #         p = t
    #     new_p = []

    #     for f in p:
    #         pp=[]
    #         pl=[]
    #         for y in f:
    #             pitch, duration = y.split()
    #             duration_float = float(duration)

    #             if duration_float > 2.0 and duration_float % 2 == 1.0:
    #                 # If duration is greater than or equal to 1.0 and odd, subtract 1.0 from it
    #                 new_duration = duration_float - 1.0
    #                 pp.append(f"{pitch} {new_duration:.1f}")
    #                 pl.append(f"{pitch} 1.0")
    #             else:
    #                 pp.append(y)
    #         new_p.append(pp)
    #         if pl:
    #             new_p.append(pl)



    #     t=new_p

    #     data = t

    #     # Find the highest value of the second item in each sublist
    #     max_values = [max(float(note.split()[1]) for note in sublist) for sublist in data]

    #     # Modify 'data' to contain the highest values as sublists
    #     durate = [[max_value] for max_value in max_values]
    #     timer = durate.copy()


    #     data = t

    #     # Remove the second items in each element in the sublists
    #     modified_data = [[note.split()[0] for note in sublist] for sublist in data]


    #     # Define the mapping of durations to names
    #     duration_names = {0.5: 'eighth',1.0: 'quarter',0.25: '16th', 2.0: 'half', 4.0: 'whole'}

    #     # Given list 'p'
    #     p = durate

    #     # Convert 'p' to their names
    #     durate = [[duration_names[d] for d in sublist] for sublist in p]

    #     data = t

    #     # Remove the second items in each element in the sublists
    #     modified_data = [[note.split()[0] for note in sublist] for sublist in data]

    #     # Define the chords as lists of note names
    #     chords = modified_data
    #     chords = [[i, *sublist] for i, sublist in enumerate(chords)]
    #     # Define the durations for each chord
    #     durations = durate
    #     # Create a stream to store the notes
    #     music_stream = stream.Stream()
    #     # music_stream.append(tempo.MetronomeMark(number=500))
    #     # Iterate through the chords and durations
    #     for i, chord_notes in enumerate(chords):
    #         if i < len(durations):
    #             chord_obj = chord.Chord(chord_notes)
    #             chord_obj.duration.type = (durations[i])[0]
    #             music_stream.append(chord_obj)
    #         else:
    #             pass
    #             # print(f"Warning: Not enough durations provided for chord {i + 1}. Skipping.")
    #     # total_duration = music_stream.duration.quarterLength
    #     # music_stream.show('midi')
    #     ##
    #     in_midi = []
    #     # if request.method == 'POST':
            
    #     #     mhb = request.POST.get('clicked_')
    #     #     print(f"mhb: {mhb}")
    #     try:
    #         # action = data.get('action')
    #         action = request.POST.get('action')

    #         if action == None:
    #             music_stream.show('midi')
    #         data = json.loads(request.body.decode('utf-8'))
    #         values = data.get('values')

    #         if len(values) == 2:
                

    #             # Extract the selected values and their colors
    #             value1 = values[0]['value']
    #             color1 = values[0]['color']
    #             value2 = values[1]['value']
    #             color2 = values[1]['color']
    #             print(value1)
    #             print(value2)
    #             if value1 > value2:
    #                 chords = chords[value2:value1]
    #                 durations = durations[value2:value1]   
    #             else:
    #                 chords = chords[value1:value2]
    #                 durations = durations[value1:value2]
    #             music_stream = stream.Stream()
    #             # music_stream.append(tempo.MetronomeMark(number=500))
    #             # Iterate through the chords and durations
    #             for i, chord_notes in enumerate(chords):
    #                 if i < len(durations):
    #                     chord_obj = chord.Chord(chord_notes)
    #                     chord_obj.duration.type = (durations[i])[0]
    #                     music_stream.append(chord_obj)
    #                 else:
    #                     pass
    #                     # print(f"Warning: Not enough durations provided for chord {i + 1}. Skipping.")
    #             # total_duration = music_stream.duration.quarterLength
    #             music_stream.show('midi')
    #             # Handle the selected objects based on their colors
    #             if color1 == 'highlight-yellow':
    #                 pass
    #                 # Handle the first selected object with a yellow highlight
    #                 # Your logic here...

    #             if color2 == 'highlight-green':
    #                 pass
    #                 # Handle the second selected object with a green highlight
    #                 # Your logic here...
    #         # For demonstration purposes, simply return the processed data
    #             return JsonResponse({'message': 'Data received and processed successfully'})
    #     except json.JSONDecodeError:
    #         # return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    #         return render(request, 'home.html', {'timer':timer, 'chords':chords, 'solta': solta})
    #     # return render(request, 'home.html', {'timer':timer, 'chords':chords})
    #     else:
    #         return render(request, 'home.html', {'timer':timer, 'chords':chords, 'solta': solta})
    #     # return render(request, 'home.html', {'timer':timer, 'chords':chords, 'solta': solta})



def index(request):
    return render(request, 'base.html')





def base(request):
    return render(request, 'lyrics/2.html')


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Only for demonstration purposes, not recommended for production
def handle_click(request):
    lists = list(range(1, 1001))
    if request.method == 'POST':
        clicked_value = request.POST.get('num')
        request.session['clicked_value'] = clicked_value
        print(clicked_value)  # For demonstration, you can use this value as needed

        # return JsonResponse({'status': 'success'})

        return render(request, 'lyrics/'+str(clicked_value)+'.html', {'lists': lists, 'clicked_value':clicked_value})
        # return render(request, 'lyricshtml', {'lists': lists})
        # return redirect('landing_page', value_one=first_value)
    return render(request, 'base.html', {'lists': lists})

    # return redirect('landing_page') + f'?value_one={first_value}'


def previous_view(request):

    first_value = "example_value"  # Replace this with your logic to get the actual value

    # Redirect to the landing page while passing the first value in the URL
    return redirect('music_view', value_one=first_value)




def one(request):
    onee= 'onee'
    return render(request, 'base.html', {'onee': onee})

def two(request):
    return render(request, 'index.html', {})





def music_view(request):

    clicked_value = request.session.get('clicked_value', None)
    print('Don')
    print(clicked_value)
    path = f"C:\\Users\\KOFI ADUKPO\\Downloads\\solfa\\{clicked_value}.xml"
    score = music21.converter.parse(path)
    # C:\Users\KOFI ADUKPO\Downloads\solfa
    # score = music21.converter.parse(path)
    # Load a MusicXML file (replace 'your_music_score.xml' with the actual file path)
    # score = music21.converter.parse("C:\\Users\\KOFI ADUKPO\\Desktop\\code\\aseda\\adom\\templates\\848.xml")


    # Initialize a list to store notes and rests at each point in time
    notes_and_rests_by_time = []
    notes_and_rests_by_time_ = []


    # Get all the notes, chords, and rests from the score
    all_notes = score.flat.getElementsByClass(music21.note.GeneralNote)

    # Create a dictionary to group elements by their starting offset
    elements_by_offset = {}

    # Iterate through the notes, chords, and rests and group them by offset
    for element in all_notes:
        offset = element.offset
        if offset not in elements_by_offset:
            elements_by_offset[offset] = []
        elements_by_offset[offset].append(element)

    # Sort the offsets in ascending order
    sorted_offsets = sorted(elements_by_offset.keys())

    notss = []

    # Iterate through the sorted offsets and collect notes and rests at each point in time
    for offset in sorted_offsets:
        elements = elements_by_offset[offset]
        notes_and_rests = []
        nots=[]

        for element in elements:
            if isinstance(element, music21.note.Note):
                pitch = element.pitch
                parts = re.split(r'(\d+)', str(pitch))
                modified_item = ''.join(parts)
                pitch = modified_item
                notes_and_rests.append(f"{pitch}") # {element.duration.quarterLength}
                nots.append(f"{pitch} {element.duration.quarterLength}")


            elif isinstance(element, music21.chord.Chord):
                for chord_note in element:
                    chord_pitch = chord_note.pitch
                    parts = re.split(r'(\d+)', str(chord_pitch))
                    modified_item = ''.join(parts)
                    chord_pitch = modified_item
                    notes_and_rests.append(f"{chord_pitch}") # {chord_note.duration.quarterLength}
                    nots.append(f"{chord_pitch} {chord_note.duration.quarterLength}")

            elif isinstance(element, music21.note.Rest):
                pass
                # notes_and_rests.append(f"Rest Duration: {element.duration.quarterLength}")

        notes_and_rests_by_time.append(notes_and_rests)
        notes_and_rests_by_time_.append(nots)
        

    # # Print the notes and rests grouped by time
    # for i, notes_and_rests in enumerate(notes_and_rests_by_time):
    #     print(f"Time {i}: {', '.join(notes_and_rests)}")

    p = [['E-4 6.0'],['C4 1.0', 'E-4 6.0', 'A-2 1.0', 'A-3 3.0'], ['C4 1.0', 'C4 2.0', 'A-2 1.0', 'A-3 2.0'], ['E-4 1.0', 'C3 1.0']]
    p=notes_and_rests_by_time_
    t = []
    main = []
    data = p
    k=p

    ##taking care of the .75
    heavy=[]
    # Check if the decimal ends with .75
    for r in k:
        qw=[]
        qe=[]
        for u in r:
            pitch, duration = u.split()
            duration_float = float(duration)
            if duration_float % 1 == 0.75:
                # Subtract 0.25 from it
                new_duration = duration_float - 0.25
                qw.append(f"{pitch} {new_duration:.1f}")
                qe.append(f"{pitch} 0.25")
            else:
                qw.append(u)
        heavy.append(qw)
        if qe:
            heavy.append(qe)

    k=heavy

    # Create a new list to store the modified elements
    # Create a new list to store the modified elements
    new_k = []

    # Iterate through the sublists in 'k'
    for sublist_k in k:
        modified_sublist = []
        remaining_sublist = []
        for element in sublist_k:
            pitch, duration = element.split()  # Split the element into pitch and duration
            duration_float = float(duration)  # Convert duration to a float
            if duration_float > 1.0:
                if duration_float % 1 == 0.5:
                    # If duration ends with '.5', subtract 0.5 and add '.0' to the duration
                    modified_duration = f"{duration_float - 0.5:.1f}"
                    modified_sublist.append(f"{pitch} {modified_duration}")
                    remaining_sublist.append(f"{pitch} 0.5")  # Add a new element with '0.5' duration
                else:
                    # If duration is odd and greater than 1.0, subtract 1.0 and create a sublist for it
                    modified_duration = f"{duration_float - 1.0:.1f}"
                    modified_sublist.append(f"{pitch} {modified_duration}")
                    remaining_sublist.append(f"{pitch} 1.0")
            else:
                # Otherwise, keep the original element in the modified sublist
                modified_sublist.append(element)
        new_k.append(modified_sublist)
        if remaining_sublist:
            new_k.append(remaining_sublist)
    p=new_k

    for i in p:


        if i:

            # Calculate the minimum duration in the list
            # print(i)
            min_duration = min(float(note.split()[1]) for note in i)

            # Create a new list with equal durations
            equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in i]
            t.append(equal_duration_list)

            # Create a remainder list with the original durations
            remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in i if float(note.split()[1]) > min_duration]
            if remainder:
                # Extract the second items from each element
                second_items = [float(note.split()[1]) for note in remainder]

                # Check if all second items are the same
                is_same_duration = all(item == second_items[0] for item in second_items)

                if is_same_duration:
                    t.append(remainder)
                else:
                    min_duration = min(float(note.split()[1]) for note in remainder) #leevel
                    # Create a new list with equal durations
                    equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
                    t.append(equal_duration_list)
                    # Create a remainder list with the original durations
                    remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in remainder if float(note.split()[1]) > min_duration]
                    # print(f'firstremain: {remainder}')
                    # Extract the second items from each element
                    if remainder:
                        second_items = [float(note.split()[1]) for note in remainder]
                        

                        # Check if all second items are the same
                        is_same_duration = all(item == second_items[0] for item in second_items)

                        if is_same_duration:
                            t.append(remainder)
                        else:
                            min_duration = min(float(note.split()[1]) for note in remainder)
                            # Create a new list with equal durations
                            equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
                            t.append(equal_duration_list)
                            ##
                            remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in remainder if float(note.split()[1]) > min_duration]
                            # Extract the second items from each element
                            # print(f'remain: {remainder}')
                            if remainder:
                                second_items = [float(note.split()[1]) for note in remainder]

                                # Check if all second items are the same
                                is_same_duration = all(item == second_items[0] for item in second_items)

                                if is_same_duration:
                                    # print(remainder)
                                    t.append(remainder)

                                else:
                                    min_duration = min(float(note.split()[1]) for note in remainder)
                                    # Create a new list with equal durations
                                    equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
                                    t.append(equal_duration_list)
                                    remainder = [f"{note.split()[0]} {float(note.split()[1]) - min_duration}" for note in remainder if float(note.split()[1]) > min_duration]

                                    if remainder:
                                        second_items = [float(note.split()[1]) for note in remainder]

                                        # Check if all second items are the same
                                        is_same_duration = all(item == second_items[0] for item in second_items)

                                        if is_same_duration:
                                            t.append(remainder)
                                        else:
                                            min_duration = min(float(note.split()[1]) for note in remainder)
                                            # Create a new list with equal durations
                                            equal_duration_list = [f"{note.split()[0]} {min_duration}" for note in remainder]
                                            t.append(equal_duration_list)



        p = t
    new_p = []

    for f in p:
        pp=[]
        pl=[]
        for y in f:
            pitch, duration = y.split()
            duration_float = float(duration)

            if duration_float > 2.0 and duration_float % 2 == 1.0:
                # If duration is greater than or equal to 1.0 and odd, subtract 1.0 from it
                new_duration = duration_float - 1.0
                pp.append(f"{pitch} {new_duration:.1f}")
                pl.append(f"{pitch} 1.0")
            else:
                pp.append(y)
        new_p.append(pp)
        if pl:
            new_p.append(pl)



    t=new_p

    data = t

    # Find the highest value of the second item in each sublist
    max_values = [max(float(note.split()[1]) for note in sublist) for sublist in data]

    # Modify 'data' to contain the highest values as sublists
    durate = [[max_value] for max_value in max_values]
    timer = durate.copy()


    data = t

    # Remove the second items in each element in the sublists
    modified_data = [[note.split()[0] for note in sublist] for sublist in data]


    # Define the mapping of durations to names
    duration_names = {0.5: 'eighth',1.0: 'quarter',0.25: '16th', 2.0: 'half', 4.0: 'whole'}

    # Given list 'p'
    p = durate

    # Convert 'p' to their names
    durate = [[duration_names[d] for d in sublist] for sublist in p]

    data = t

    # Remove the second items in each element in the sublists
    modified_data = [[note.split()[0] for note in sublist] for sublist in data]

    # Define the chords as lists of note names
    chords = modified_data
    chords = [[i, *sublist] for i, sublist in enumerate(chords)]
    # Define the durations for each chord
    durations = durate
    # Create a stream to store the notes
    music_stream = stream.Stream()
    # music_stream.append(tempo.MetronomeMark(number=500))
    # Iterate through the chords and durations
    for i, chord_notes in enumerate(chords):
        if i < len(durations):
            chord_obj = chord.Chord(chord_notes)
            chord_obj.duration.type = (durations[i])[0]
            music_stream.append(chord_obj)
        else:
            pass
            # print(f"Warning: Not enough durations provided for chord {i + 1}. Skipping.")
    # total_duration = music_stream.duration.quarterLength
    # music_stream.show('midi')
    ##
    in_midi = []
    if request.method == 'POST':

        try:
            # action = data.get('action')
            action = request.POST.get('action')

            if action == None:
                music_stream.show('midi')
            data = json.loads(request.body.decode('utf-8'))
            values = data.get('values')

            if len(values) == 2:
                

                # Extract the selected values and their colors
                value1 = values[0]['value']
                color1 = values[0]['color']
                value2 = values[1]['value']
                color2 = values[1]['color']
                print(value1)
                print(value2)
                if value1 > value2:
                    chords = chords[value2:value1]
                    durations = durations[value2:value1]   
                else:
                    chords = chords[value1:value2]
                    durations = durations[value1:value2]
                music_stream = stream.Stream()
                # music_stream.append(tempo.MetronomeMark(number=500))
                # Iterate through the chords and durations
                for i, chord_notes in enumerate(chords):
                    if i < len(durations):
                        chord_obj = chord.Chord(chord_notes)
                        chord_obj.duration.type = (durations[i])[0]
                        music_stream.append(chord_obj)
                    else:
                        pass
                music_stream.show('midi')


                # Handle the selected objects based on their colors
                if color1 == 'highlight-yellow':
                    pass
                    # Handle the first selected object with a yellow highlight
                    # Your logic here...

                if color2 == 'highlight-green':
                    pass
                    # Handle the second selected object with a green highlight
                    # Your logic here...
                # music_stream.stop()

            # For demonstration purposes, simply return the processed data
                return JsonResponse({'message': 'Data received and processed successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        # return render(request, 'home.html', {'timer':timer, 'chords':chords})
    else:
        return render(request, 'home.html', {'timer':timer, 'chords':chords})
        # return JsonResponse({'error': 'Invalid request method'}, status=405)





